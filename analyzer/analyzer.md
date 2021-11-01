# COORDINATES RECOGNITION

The new recognizer implemented is based on the PatternRecognizer class, since it supports regex based recognition.

The CoordinatesRecognizer class, as a matter of fact, is composed of a list of regular expression :

- Decimal Degrees Coordinates: `[-+]?([1-8]?\d(\.\d+)|90(\.0+)?),\s*[-+]?(180(\.0+)|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)`

- Latitude: `([1-8]?\d(\.\d+)|90(\.0+)?)[N|S]` or `[N|S]([1-8]?\d(\.\d+)|90(\.0+)?)`
- Longitude: `[E|W](180(\.0+)|((1[0-7]\d)|([1-9]?\d))(\.\d+))` or `(180(\.0+)|((1[0-7]\d)|([1-9]?\d))(\.\d+))[E|W]`
- Degrees Minutes Seconds: `((\d+)\s?\º|((\d+)\s?\˜°|((\d+)\s?\°)|(\d+)\s?\˚))\s?((\d+)\s?\’|(\d+)\s?\')?\s?((\d{1,}\.?\,?\d{0,}?)\")?\s?[N,S,E,W]` or `[N,S,E,W]((\d+)\s?\º|((\d+)\s?\˜°|((\d+)\s?\°)|(\d+)\s?\˚))\s?((\d+)\s?\’|(\d+)\s?\')?\s?((\d{1,}\.?\,?\d{0,}?)\")?`


## Installation 

### Working Enviroment:
`$ pip install presidio_analyzer`

`$ python -m spacy download en_core_web_lg`

`$ git clone https://github.com/btessa99/microsoft_presidio.git`

Add coordinates_recognizer.py to presidio_analyzer/predefined_recognizers

Add the recognizer to the recognizers_map dict in the RecognizerRegistry.load_predefined_recognizers method located in presidio_analyzer/recognizer.

The recognizer_map should look like this:
```
    recognizers_map = {
            "en": [
                UsBankRecognizer,
                UsLicenseRecognizer,
                UsItinRecognizer,
                UsPassportRecognizer,
                UsPhoneRecognizer,
                UsSsnRecognizer,
                NhsRecognizer,
                SgFinRecognizer,
  
            ],
            "es": [EsNifRecognizer],
            "ALL": [
                CreditCardRecognizer,
                CryptoRecognizer,
                DateRecognizer,
                DomainRecognizer,
                EmailRecognizer,
                IbanRecognizer,
                IpRecognizer,
                MedicalLicenseRecognizer,
                CoordinatesRecognizer,
                nlp_recognizer,
            ],
        }
```
Where CoordinatesRecognizer is our new recognizer.

## An Example

Let's take a look at the content of the file demo_coord1.txt

`The city center of Abeokuta lies approximately on latitude 7° 30' N and longitude 30° 54' E. the humid lowland rain forest region with two distinctive seasons`

and let's try to analyze it:

```
analyzer = AnalyzerEngine(registry=registry)

results = analyzer.analyze(text, language="en")

```

If we print the variable `result`, this will be the output:

`[type: LOCATION, start: 19, end: 27, score: 0.85, type: GEO_COORDINATES, start: 59, end: 67, score: 0.6, type: GEO_COORDINATES, start: 82, end: 91, score: 0.6]`
























