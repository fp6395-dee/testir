# testir

Ultimate Tic-Tac-Toe (9x9, 9 pod-poley 3x3).

## Pravila (korotko)

- Pole 9x9 razbito na 9 pod-poley 3x3.
- Pervyy hod - v lyubuyu kletku.
- Dalee kazhdyy hod opredelyaet, v kakoe pod-pole obyazan igrat sopernik
  (po koordinate kletki vnutri tekuschego pod-polya).
- Esli ukazannoe pod-pole uzhe vyigrano ili zapolneno, sopernik hodit
  v lyuboe svobodnoe pod-pole.
- Pobeda - sobrat 3 svoih pod-polya v ryad (po gorizontal, vertikal ili
  diagonali).

## Zapusk

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python -m src.main

## Testy

    pytest -q
