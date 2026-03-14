using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LetterHolder : MonoBehaviour
{
    // class holds and manages tile holders in phase two
    [SerializeField] private int numPerRow;
    [SerializeField] private TileHolder[] tileHolders;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    public void deleteLetters()
    {
        List<LetterScript> letterScripts = new List<LetterScript>();
        List<SpellTile> spellTiles = new List<SpellTile>();
        foreach(TileHolder tileHolder in tileHolders)
        {
            letterScripts.AddRange(tileHolder.letterScripts);
            spellTiles.AddRange(tileHolder.spells);
            tileHolder.clearLists();
        }
        foreach(LetterScript letterScript in letterScripts)
        {
            Destroy(letterScript.gameObject);
        }
        foreach (SpellTile spellTile in spellTiles)
        {
            Destroy(spellTile.gameObject);
        }
    }

    public bool hasNoTiles()
    {

        if (tileHolders[0].numTiles() == 0)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    // Update is called once per frame
    void Update()
    {

        for (int i = 0; i < tileHolders.Length; i++)
        {
            // move tiles down if past limit
            if (tileHolders[i].numTiles() > numPerRow)
            {
                if (i + 1 != tileHolders.Length)
                {
                    tileHolders[i].giveTile(tileHolders[i].lastTile(), tileHolders[i + 1]);
                }
                else
                {
                    Debug.Log("Limit reached");
                }
            }
            // move tile down if under limit
            else if (tileHolders[i].numTiles() < numPerRow)
            {
                if (i + 1 != tileHolders.Length)
                {
                    if (tileHolders[i + 1].numTiles() > 0)
                    {
                        tileHolders[i + 1].giveTile(tileHolders[i + 1].lastTile(), tileHolders[i]);
                    }
                }
            }
        }

    }
}
