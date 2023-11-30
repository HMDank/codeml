INSTRUCTION:

1. Make sure you've read and followed through requirements.txt
2. Once finished with installing and setting up IDE, open Test7.ipynb
2.1 In the second box (df = pd.read_csv('path')), replace path with file path to .csv file
2.2 Run the program (via the "Run All" button, or shift-entering all the way through)
3. Open please.py and navigate to that file (by choosing directory) through the terminal, and run the API with "python -m uvicorn please:app --reload"
4. Ctrl + Click HTTP link the API provided (Or open browser of choice and paste in the URL bar: "http://127.0.0.1:8000")
5. Add "/docs" at the end of URL to navigate to the main page
6. Expand "/predict" tab, following by "try it out"
7. Input all the needed data right below that
8. Execute
9. Navigate to the Response Body and...

Voila, there's the desired car price prediction.