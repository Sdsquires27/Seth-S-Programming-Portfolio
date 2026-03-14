using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WordMaker : MonoBehaviour
{
    LetterScript[] letters;
    WordGameDict dict = new WordGameDict();
    [SerializeField] UnitCreator unitCreator;
    string currentWord()
    {
        // finds and returns the current word being spelled
        string word = "";
        letters = GetComponentsInChildren<LetterScript>();
        foreach(LetterScript letter in letters)
        {
            word += letter.letter.character;
        }
        return word;
    }

    public void endTurn()
    {
        GameManager.instance.switchTurns();
    }

    public void submitWord()
    {
        if (dict.CheckWord(currentWord(), 2))
        {
            GameManager.instance.giveWordPoints(currentWord());
            // do the thing
            Unit unit = new Unit(currentWord(), letters);

            unitCreator.addUnit(unit);
            foreach (LetterScript letter in letters)
            {
                Destroy(letter.gameObject);
            }
            
        }
        else
        {
            cancelWord();
        }

    }

    public void cancelWord()
    {
        foreach(LetterScript letter in letters)
        {
            letter.gameManager.handleTileClick(letter);
        }
    }


    // Start is called before the first frame update
    void Start()
    {
        dict.InitializeDictionary();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
