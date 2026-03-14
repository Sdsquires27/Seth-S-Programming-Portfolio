using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

[System.Serializable]
public class Unit
{
    // holds unit data
    public string word;
    public Sprite sprite;
    public LetterScript[] letterScripts;
    public List<Letter> letters = new List<Letter>();
    public int worth;
    public int hpMax;
    public int armor;
    public int piercing;
    public int pierceMin = 0;
    public int moveSpeed;
    public int range;
    public int dmg;
    public int hpMin = 1;
    public int armorMin = 0;
    public int moveSpeedMin = 1;
    public int dmgMin = 1;
    public int spellSlots = 0;
    public bool moveAfterAttack = false;
    public List<SpellTile> spellTiles = new List<SpellTile>();
    public List<Action> spells = new List<Action>();

    public Unit(string setWord, LetterScript[] setLetters, Sprite sprite)
    {
        // create a standard unit
        letterScripts = setLetters;
        this.sprite = sprite;
        word = setWord;
        hpMax = 1;
        armor = 0;
        moveSpeed = 1;
        range = 1;
        dmg = 1;
        piercing = 0;
        getLetters();
        getStats();
    }

    public Unit(string setWord, LetterScript[] setLetters)
    {
        // create a standard unit
        letterScripts = setLetters;
        sprite = GameManager.findSprite(setWord);
        word = setWord;
        hpMax = 1;
        armor = 0;
        moveSpeed = 1;
        range = 1;
        dmg = 1;
        piercing = 0;
        getLetters();
        getStats();
    }

    public void generateSpells()
    {
        foreach(SpellTile spellTile in spellTiles)
        {
            spells.Add(Resources.Load<Action>("Spells/"+spellTile.name));
            
        }
        foreach(Action spell in spells)
        {

        }
    }

    public void printDescription()
    {
        string toPrint = "UNIT " + word + "\n";

        toPrint += "Hp: " + hpMax + "\n" +
            "Dmg: " + dmg + "\n" +
            "Armor: " + hpMax + "\n" +
            "MoveSpeed: " + hpMax + "\n" +
            "Piercing: " + hpMax + "\nSpells:";
        foreach (Action spell in spells)
        {
            toPrint += "\n" + spell;
        }

        

    }

    private void getLetters()
    {
        foreach (LetterScript letter in letterScripts)
        {
            letters.Add(letter.letter);
        }
    }

    private void getStats()
    {
        foreach (Letter letter in letters)
        {
            if(letter.worth == 1)
            {
                worth += 1;
            }
            else if (letter.worth == 2)
            {
                worth += 1;
                giveRandomStat();
            }
            else if (letter.worth == 3)
            {
                worth += 2;
            }
            else if (letter.worth == 4)
            {
                worth += 1;
                spellSlots += 1 ;
            }
            else if(letter.worth == 5)
            {
                worth += 2;
                range += 1;
            }
            else if(letter.worth == 6)
            {
                worth += 3;
                moveAfterAttack = true;
            }
            else if (letter.worth == 7)
            {
                worth += 2;
                spellSlots += 2;
            }
            else if(letter.worth == 8)
            {
                worth += 4;
            }

        }
        if(letters.Count >= 4)
        {
            worth += 1;

            if (letters.Count >= 5)
            {
                spellSlots += 1;

                if (letters.Count >= 6)
                {
                    worth += 2;

                    if (letters.Count >= 7)
                    {
                        worth += 1 * (letters.Count - 6);
                    }
                }
            }
        }

        if(word == "SETH")
        {
            worth += 10; // hehe
        }
    }

    public void giveRandomStat()
    {
        int rand = Random.Range(0, 4);

        if (rand == 0)
        {
            hpMax += 2;
            hpMin += 2;
        }
        else if(rand == 1)
        {
            armor += 1;
            armorMin += 1;
        }
        else if (rand == 2)
        {
            dmg += 1;
            dmgMin += 1;
        }
        else if (rand == 3)
        {
            moveSpeed += 1;
            moveSpeedMin += 1;
        }
        else if (rand == 4)
        {
            piercing += 1;
            pierceMin += 1;
        }
           
        
    }
}
