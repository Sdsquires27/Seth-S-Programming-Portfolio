using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PlayerController : MonoBehaviour
{
    [Header("Components")]
    [SerializeField] private GameObject horizontalLayout;
    [SerializeField] private GameObject layoutGroup;
    [SerializeField] private GameObject spellGroup;

    [Header("Settings")]
    [SerializeField] private int maxLetters;
    [SerializeField] public Color color;

    [System.NonSerialized] public int score = 0;
    //[System.NonSerialized] 
    public string playerName;


    private List<LetterScript> heldTiles = new List<LetterScript>();
    [System.NonSerialized] public List<Unit> unitList = new List<Unit>();
    private List<SpellTile> heldSpells = new List<SpellTile>();
    private int lettersInGroup = 0;
    private GameObject curLayout;


    public string getLetters()
    {
        string letters = "";

        foreach (LetterScript tile in heldTiles)
        {
            letters += tile.letter.character;
        }

        return letters;
    }

    public void subtractScore(int difference)
    {
        score -= difference;
    }

    public void addScore(int amount)
    {
        score += amount;
    }

    public List<string> getSpells()
    {
        List<string> spells = new List<string>();
        foreach (SpellTile tile in heldSpells)
        {
            spells.Add(tile.packName());
        }
        return spells;
    }

    private void Start()
    {
        layoutGroup = GameObject.FindGameObjectWithTag(name);
        curLayout = Instantiate(horizontalLayout, layoutGroup.transform);
    }

    public void addTile(LetterScript newLetter)
    {
        heldTiles.Add(newLetter);
        newLetter.transform.SetParent(curLayout.transform);
        lettersInGroup++;
        if (lettersInGroup == maxLetters)
        {
            lettersInGroup = 0;
            curLayout = Instantiate(horizontalLayout, layoutGroup.transform);
        }
    }

    public void addTile(SpellTile newSpell)
    {
        heldSpells.Add(newSpell);
        newSpell.transform.SetParent(curLayout.transform);
        lettersInGroup++;
        if (lettersInGroup == maxLetters)
        {
            lettersInGroup = 0;
            curLayout = Instantiate(horizontalLayout, layoutGroup.transform);
        }
    }

}
