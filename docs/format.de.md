# Katalogformat 2: Referenz (DE) · [English](format.md)

`packages.toml` sagt, was angeboten wird; `python3 scripts/gen_catalog.py` liest die öffentlichen Releases und schreibt `catalog.xml`
(AppStream-Sammlung, von der CI signiert). Format 2 ergänzt, was der Store je Paket zeigt. Jedes neue Feld ist für den Leser optional:
ein alter Eintrag bleibt gültig, der Store zeigt „unbekannt“ für das, was fehlt.

Prüfen ohne Netz (und ohne zu schreiben): `python3 -I scripts/gen_catalog.py --check [packages.toml] [--capabilities DATEI]`.
Alle Befunde auf einmal als `<Paket>: <Feld>: <Meldung>`; Fehler stoppen den Lauf, Warnungen nicht.

## Dateiebene
| Schlüssel | Bedeutung |
|---|---|
| `schema` | `1` (Vorgabe) oder `2`. Mit `2` sind die unten mit „Format 2“ markierten Regeln **Fehler**, mit `1` Warnungen (die wöchentliche Signierung hält für einen alten Eintrag nie an). Der Katalog bekommt `fs-schema="2"` an `<components>`. |
| `capabilities_ref` | Tag (Form `vX.Y.Z`, geprüft) von `fs-interfaces`, dessen `schema/capabilities.txt` DIE Fähigkeitenliste ist (Vorgabe `v0.0.21`). Wird mit `gh api` gelesen, nie in dieses Repo kopiert. `--capabilities DATEI` / `$FS_CAPABILITIES_FILE`: lokale Datei (offline). |

## Je Paket (`[[package]]`)
Unter-Tabellen (`[package.x]`, `[[package.x]]`) **nach** den einfachen Schlüsseln des Pakets schreiben: `bump_catalog.py` ändert `tag` als Text.

| Schlüssel | XML | Regel |
|---|---|---|
| `id`, `name`, `summary`, `repo`, `tag`, `asset` | wie bisher | Pflicht; `id` klein geschrieben; `tag` `vMAJOR.MINOR.PATCH` (Wrapper: `v<Upstream>[-fs<N>]`, siehe unten) |
| `kind` | `fs:kind`, `type` der Komponente | `program` (Vorgabe), `frontend`, `component`, `theme`, `server`, `icon-theme`. AppStream-Typ: program/frontend `desktop-application`, component/theme `addon`, server `service`, icon-theme `icon-theme`. `server` und `icon-theme` sind neu. Heutige Stores (vor 0.0.13) **verwerfen** so einen Eintrag („unknown fs:kind“, als übersprungen gelistet; Katalog und andere Pakete bleiben heil); ein gesperrtes Angebot „von dieser Store-Version nicht unterstützt“ zeigen erst Stores ab 0.0.13 (Leser-Korrektur in Arbeit). `min_store` schützt erst ab Store 0.0.13: ältere Stores ignorieren `fs:min-store` bei Arten, die sie kennen (program usw.); bei unbekannten Arten lassen sie den Eintrag nur aus (übersprungen), sie brechen nicht. Deshalb werden sie nur mit `schema = 2` UND `min_store` geschrieben und kommen erst in den ECHTEN Katalog, NACHDEM ein Store mit dem korrigierten Leser veröffentlicht ist. |
| `description` | `<description>` | Text oder Tabelle `{ en = "..", de = ".." }` (Sprachvarianten EINER Beschreibung, `xml:lang`; `en` Pflicht, wird zuerst geschrieben). Leerzeile = neuer Absatz. Format 2: Pflicht (Rückfall des Stores). |
| `icon`, `icon_sha256` | `<icon type="remote" fs-sha256>` | https-Adresse eines **PNG bis 1 MiB** (SVG wird abgelehnt, wie im Store). Der Generator lädt es, prüft die PNG-Kennung, schreibt den SHA-256 (und vergleicht mit `icon_sha256`, falls angegeben). Format 2: **Pflicht für jedes Paket**. |
| `provides`, `requires`, `recommends` | `fs:provides` ... | Liste von Fähigkeiten `"name"` oder `"name major.minor"` (auch `name>=1.2`). Namen NUR aus `capabilities.txt` von fs-interfaces; unbekannter Name = Fehler mit „meintest du“. Ein `planned`-Name ist eine Warnung. Ohne Stufe = beliebig. Getrennt von Rechten. |
| `[[package.feature]]` | `fs:features`, `fs:feature.<key>.provides/requires/recommends/name` | ein Merkmal: `key` (Pflicht), `name` und eigene `provides`/`requires`/`recommends`. Darf leer bleiben (nur `key`). |
| `mediatypes` | `<provides><mediatype>` | Liste wie `["text/calendar"]` (wie AppStream). |
| `installed_size` | `<size type="installed">` | Tabelle `{ "0.0.7" = Bytes }`; nur der Eintrag der angebotenen Version wird geschrieben (der Tag wandert von selbst, die Zahl darf nicht veralten). |
| (von GitHub) | `<size type="download">` | Größe der Release-Datei aus dem Release; auch bei rpm/deb/exe. |
| `[[package.history]]` | `<release version date><description xml:lang>` | je Release: `version`, `changes` (Text oder Sprachtabelle, `en` Pflicht), `date` `JJJJ-MM-TT` (bei älteren Releases Pflicht). Der Eintrag der angebotenen Version ist der Text des aktuellen Releases (Datum von GitHub). Ältere werden Releases ohne Dateien (nur Änderungsliste). Kein Eintrag zur aktuellen Version = Warnung (nie Fehler: `bump` hebt Tags allein an). |
| `upstream` | `fs:upstream` | https-Adresse, unter der der Macher es veröffentlicht (Quelle der Spiegelung). |
| `upstream_signature` | `fs:upstream-signature` | Signatur des Machers: Schlüssel-Fingerabdruck (hex) oder https-Adresse; braucht `upstream`. |
| `source_code` | `fs:source-code` | https-Adresse des Quellcodes dieser Version. Format 2: Pflicht, wenn `upstream` gesetzt ist (ADR 0068, mit dem Paket gespiegelt). |
| `maker` | `fs:maker` | Name des Machers. |
| `[package.description_wiki]` | `fs:description-wiki` (Block-Id), `-source-rev`, optional `-lang` | ADR 0072, Nutzerentscheid: DE/EN sind EINE Seite mit Sprachvarianten, also EINE Block-Id (UUIDv7); die Varianten liegen im Block. `block`, `source_rev` (Zahl, Pflicht: die Fassung, aus der der Eintrag gemacht wurde, damit der Store merkt, dass das Wiki weiter ist), `lang` optional (nur Wunsch beim Lesen, nie ein zweiter Block). Kein `translationOf`, keine Block-Id je Sprache. Die Textbeschreibung bleibt Rückfall. |
| `min_store` | `fs:min-store` | erste fs-store-Version, die den Eintrag liest, `MAJOR.MINOR.PATCH`. **Pflicht bei `server` und `icon-theme`**, die nur mit `schema = 2` geschrieben werden. |
| `[[package.screenshot]]` | `<screenshots><screenshot><image type="source" fs-sha256 fs-license fs-source><caption xml:lang>` | `url` https, `license` klar (SPDX-Id; `unknown`, `none`, `proprietary`, `all rights reserved` und seltsame Zeichen werden abgelehnt: **ohne klare Lizenz kein Bild**), `source` (Adresse oder Macher), `caption` (Text oder Sprachtabelle), `sha256` optional (wird geladen und verglichen; der berechnete Hash wird geschrieben). PNG, JPEG oder WebP, höchstens 5 MiB. Das erste Bild ist das Standardbild. |

Je Art (Format 2): `program` und `server` brauchen `provides`; `frontend` braucht `requires`; `theme`, `icon-theme`, `component` nichts Zusätzliches.

## Wrapper: `v<Upstream-Version>` und `-fs<N>`
`vMAJOR.MINOR.PATCH` ist der Tag **eigener** Programme (ADR 0064). Ein Paket, das ein **fremdes** Programm einwickelt (Spiegel, ADR 0068; bisher `kind = "server"`,
die Regel hängt aber nicht von der Art ab), übernimmt die Upstream-Version **unverändert** in seinen Tag und muss `upstream` nennen (daran unterscheidet der
Generator es von einem eigenen Programm):
- erster Bau einer Upstream-Version: `v<Upstream-Version>`, z. B. `v26.11_2` (Upstream Zentinel `26.11_2`), `v1.12.1` (Upstream Kanidm `1.12.1`);
- jeder weitere Bau UNSERES Pakets derselben Upstream-Version: `v<Upstream-Version>-fs<N>` mit N >= 2, z. B. `v26.11_2-fs2`, `v1.12.1-fs2`.
  `-fs1` gibt es nicht (Bau 1 hat kein Suffix); `N` ohne führende Null. Eine neue Upstream-Version beginnt wieder ohne Suffix.

Der Upstream-Anteil darf `.`, `_`, `-`, `+`, `~`, ASCII-Buchstaben und ASCII-Ziffern 0-9 enthalten (beginnt mit einer Ziffer, endet mit Buchstabe oder Ziffer) und wird nie verändert oder
zerlegt; die Regel ist also für jeden Upstream gleich. `-fs` kommt in keiner uns bekannten Upstream-Version vor; enthielte eine `-fs`, wird sie **abgelehnt**
(die Regel wäre nicht mehr eindeutig), ebenso ein zweites `-fs`-Suffix. Nur das kleingeschriebene `-fs` bildet das Suffix: `v1.0-Fs2` ist Bau 1 der Upstream-Version `1.0-Fs2`. Ein Zeilenumbruch am Ende wird abgelehnt. Die Katalogversion ist der Tag ohne `v` (`26.11_2-fs2`).
Paketdateien behalten die native Revision ihres Formats (`zentinel_26.11.2-1_amd64.deb`). `min_store` und `schema` bleiben `MAJOR.MINOR.PATCH`.
Bestehende Tags werden nicht umbenannt. Reihenfolge (bump, Verlauf), wie bei rpm/dpkg: zuerst nach Upstream-Version, dann nach `N`. Zahlen werden numerisch von links nach rechts verglichen, `_` wie `.`
(`26.11_3` nach `26.11_2`, vor `27.0`); ein Wort (rc, alpha, beta, beliebige Buchstaben) vor dem Ende der Version ist ein Vorabkennzeichen und sortiert **vor** derselben
Version ohne es: `1.0~rc1` < `1.0-rc1` < `1.0` < `1.0.1`, `rc1` < `rc2` < `rc10`, `alpha` < `beta` < `rc` (Wörter ohne Beachtung der Groß-/Kleinschreibung); `~` sortiert vor allem,
auch vor dem Ende; ein `+build`-Teil wird ignoriert. Preis: `1.1.1a` < `1.1.1` (Schreibweise von OpenSSL). bump geht also nie von einer finalen Version auf einen Vorabstand zurück.
Wechselt ein Upstream sein Schema, übernimmt bump die neue Version nicht; ein Mensch setzt den Tag. Ein Paket mit `upstream` nimmt nur Wrapper-Tags, eines ohne nur `vMAJOR.MINOR.PATCH`; die Familien werden nie gemischt.

Ein Paket kann Format 2 allein verlangen: `schema = 2` in seiner `[[package]]`-Tabelle macht die Regeln von Format 2 nur für dieses Paket zu Fehlern, während die
Datei für ältere Einträge bei `schema = 1` bleibt. Ein `server` wird nur angeboten, wenn sein Release ein signiertes rpm oder deb hat (ADR 0077 Abschnitt 3); sonst überspringt ihn der Generator.
Das neutrale Server-Icon ist `icons/server.png` (CC0, erzeugt von `icons/make_icons.py`).

## Downloads und Fehler
Icons und Bilder werden nur über https geladen (auch nach Weiterleitungen, `--proto =https --proto-redir =https`, höchstens 3), mit Größengrenze; der ERSTE Host wird abgelehnt, wenn er auf eine Loopback- oder private Adresse aufgelöst wird (eine Weiterleitung, höchstens 3 und nur https, oder DNS-Rebinding zwischen dieser Prüfung und dem Download ist **nicht** abgedeckt: der Generator läuft auf einem GitHub-Runner ohne interne Dienste und liest nur öffentliche Bilder); der Dateityp wird an den ersten Bytes geprüft (WebP nur mit `WEBP` ab Byte 8; kein SVG, kein XML). Ein **fehlgeschlagener Download hält bump und sign nie an**: das Paket wird mit Warnung übersprungen, der Eintrag des letzten signierten Katalogs bleibt. Eine falsche Datei (kein Bild, Hash weicht ab, zu groß) ist ein Fehler. Unter `schema = 1` sind falsche Fähigkeitsnamen nur Warnungen, und die Liste wird nur von GitHub gelesen, wenn ein Paket eine Fähigkeit nennt (nicht lesbar: Warnung).

## Was der Store liest (siehe `fs_store_catalog::Details`)
`<size type="download">` des Artefakts, `<release date>`, die erste `<description>` des Releases (Englisch), `fs:provides/requires/recommends`
(Kommaliste, `name major.minor`), `fs:upstream*`, `fs:source-code`, `fs:description-wiki` (der ganze Wert ist die Block-Id), `<icon>`, `<screenshot>`
(https + `fs-sha256` + klare `fs-license`, sonst zurückgehalten). Noch nicht vom Store gelesen (siehe CHANGES-FOR-STORE.md): Wahl nach `xml:lang`,
`<size type="installed">`, `fs:maker`, `fs-source`, `fs:feature.*`, `<provides><mediatype>`, `fs:description-wiki-source-rev`/`-lang`, Arten `server`/`icon-theme`.

## Beispiele und Tests
`examples/packages.example.toml` zeigt jedes Feld; `examples/catalog.example.xml` ist, was der Generator daraus macht (offline, von den Tests geprüft);
`examples/make_images.py` erzeugt die Bilder (für dieses Repo erzeugt, CC0-1.0). Tests: `python3 -I -m unittest discover -s tests`.
Goldene Datei nach gewollter Änderung erneuern: `python3 -I tests/support.py --write-golden`.
