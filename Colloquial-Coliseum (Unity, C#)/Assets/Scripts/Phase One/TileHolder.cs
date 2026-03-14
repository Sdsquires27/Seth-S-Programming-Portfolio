using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TileHolder : MonoBehaviour
{
    // Class used during phase one
    // holds tiles in horizontal layout and flips them when needed

    // tiles held by this holder
    [System.NonSerialized] public List<LetterScript> letterScripts = new List<LetterScript>();
    [System.NonSerialized] public List<SpellTile> spells = new List<SpellTile>();

    // Start is called before the first frame update
    void Start()
    {
        
    }

    public string getLetters()
    {
        string letters = "";

        foreach (LetterScript tile in letterScripts)
        {
            letters += tile.letter.character;
        }

        return letters;
    }

    public List<string> getSpells()
    {
        List<string> spellNames = new List<string>();
        foreach (SpellTile tile in spells)
        {
            spellNames.Add(tile.packName());
        }
        return spellNames;
    }

    public void flipTiles()
    {
        foreach (LetterScript letterScript in letterScripts)
        {
            letterScript.flip();
        }
    }
    public void hideTiles()
    {
        foreach (LetterScript letterScript in letterScripts)
        {
            letterScript.hide();
        }
    }
    public void revealTiles()
    {
        foreach (LetterScript letterScript in letterScripts)
        {
            letterScript.show();
        }
    }

    public void removeTile(LetterScript tileToRemove)
    {
        letterScripts.Remove(tileToRemove);
        tileToRemove.tileHolder = null;
    }

    public void addTile(LetterScript tileToAdd)
    {
        letterScripts.Add(tileToAdd);
        tileToAdd.tileHolder = this;
        tileToAdd.transform.SetParent(transform);
    }

    public void giveTile(LetterScript tileToGive, TileHolder newHolder)
    {
        removeTile(tileToGive);
        newHolder.addTile(tileToGive);
        tileToGive.transform.SetParent(newHolder.transform);
        tileToGive.tileHolder = newHolder;
    }

    public void clearLists()
    {
        spells.Clear();
        letterScripts.Clear();
    }

    public void removeTile(SpellTile tileToRemove)
    {
        spells.Remove(tileToRemove);
        tileToRemove.spellHolder = null;
    }

    public void addTile(SpellTile tileToAdd)
    {
        spells.Add(tileToAdd);
        tileToAdd.spellHolder = this;
        tileToAdd.transform.SetParent(transform);
    }


    public LetterScript lastTile()
    {
        return letterScripts[letterScripts.Count - 1];
    }

    public int numTiles()
    {
        return letterScripts.Count + spells.Count;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
