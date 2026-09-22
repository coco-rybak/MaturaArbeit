# Datenformat für Kletterrouten

Die Routendaten sind ein JSON-Objekt, das Listen mit Griffen und Routen enthält.

| Field | Type | Beschreibung |
| :--- | :--- | :--- |
| `holds` | `Array` | Eine Liste aller verfügbaren Griffe an der Wand. |
| `route` | `Array` | Eine sortierte Liste von `id`-Zeichenketten aus dem Array „holds“. |

**Objektstruktur eines Klettergriffs:**
*   `id` (string): eindeutige Kennung (e.g., "h21").
*   `x` (int): horizontale Koordinate.
*   `y` (int): vertikale Koordinate.
*   `type` (string): Kategorie des Klettergriffs (`jug`, `crimp`, `sloper`, etc).

## Automation

Wir definieren ein JSON-Schema, das es Tools (wie VS Code und PyCharm) ermöglicht, beim manuellen Erstellen eine Autovervollständigungshilfe anzuzeigen. Ausserdem ist es dann möglich, die manuell erstellten Routendaten über die Befehlszeile zu validieren, wie unten gezeigt:

``` Bash
# Wenn korrekt:
$ uvx check-jsonschema --schemafile wall-schema.json wall-route-sample-01.json
ok -- validation done

# Bei Fehlern:
$ uvx check-jsonschema --schemafile wall-schema.json wall-route-sample-01.json
Schema validation errors were encountered.
  wall-route-sample-01.json::$.holds[1]: 'y' is a required property
```