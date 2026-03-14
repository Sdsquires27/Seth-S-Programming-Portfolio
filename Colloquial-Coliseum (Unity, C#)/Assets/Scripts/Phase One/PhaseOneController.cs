using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using UnityEngine.UI;

public class PhaseOneController : MonoBehaviour
{
    // !! THIS CLASS HAS BEEN MOVED TO GAME CONTROLLER !! //


    // controls the first phase of gameplay
    private List<char> chars = new List<char>();
    [System.NonSerialized] public int numLetters;
    [SerializeField] private LetterScript letterPrefab;
    [SerializeField] private int lettersPerRow;
    [SerializeField] private GameObject layoutPrefab;
    [SerializeField] private PlayerController[] playerList;
    List<GameObject> horizontalLayouts = new List<GameObject>();
    [System.NonSerialized] public PlayerController curPlayer;

    private GameObject canvas;
    private int playerNum = 0;
    private int curTileGroup = 0;
    private int numPlayers;
    private GameManager gameManager;
    int numPicks = 0;

    // Start is called before the first frame update
    void Start()
    {

    }

/*    void startPhaseOne()
    {
        gameManager = FindObjectOfType<GameManager>();
        numPlayers = gameManager.numPlayers;
        numLetters = lettersPerRow * (numPlayers + 1);
        curPlayer = playerList[0];
        for (int i = numPlayers; i < playerList.Length; i++)
        {
            playerList[i].enabled = false;
        }

        //create a vertical layout group that holds the horizontal layout groups which hold the tiles
        GameObject verticalLayout = new GameObject();
        VerticalLayoutGroup verticalLayoutGroup = verticalLayout.AddComponent<VerticalLayoutGroup>();
        verticalLayoutGroup.spacing = 20;

        // add new vertical layout to 
        verticalLayout.transform.SetParent(canvas.transform);
        verticalLayout.transform.localPosition = new Vector3(0, 200, 0);
        verticalLayoutGroup.childAlignment = TextAnchor.UpperCenter;

        // grab the letters from the folder in resources
        Letter[] files = Resources.LoadAll<Letter>("Letters");

        // for each letter, add a corresponding number of characters to the pot
        foreach (Letter letter in files)
        {
            for (int i = 0; i < letter.amount; i++)
            {
                chars.Add(letter.character);
            }
        }

        // make new horizontal layout to hold tiles
        for (int i = 0; i < numLetters / lettersPerRow; i++)
        {
            GameObject temp = Instantiate(layoutPrefab, verticalLayout.transform);
            horizontalLayouts.Add(temp);
        }
        int layoutChildren = 0;
        int curLayout = 0;
        for (int i = 0; i < numLetters; i++)
        {
            // once horizontal layout is full, create new layout
            if (layoutChildren == lettersPerRow)
            {
                curLayout++;
                layoutChildren = 0;
            }

            // create new letter tile
            LetterScript x = Instantiate(letterPrefab, transform.position, Quaternion.identity);

            // generate random letter for tile and remove that letter from the list
            int randNum = Random.Range(0, chars.Count - 1);
            char randChar = chars[randNum];
            chars.RemoveAt(randNum);

            // find which letter matches the character
            Letter letter = Resources.Load<Letter>("Letters/" + randChar.ToString());
            // give the new letter tile that letter
            x.letter = letter;

            // place the letter inside the horizontal layout
            x.transform.SetParent(horizontalLayouts[curLayout].transform);
            horizontalLayouts[curLayout].GetComponent<TileHolder>().letterScripts.Add(x);
            layoutChildren++;


            // initialize the letter
            x.initialize(this, horizontalLayouts[curLayout].GetComponent<TileHolder>());
        }


        horizontalLayouts[0].GetComponent<TileHolder>().flipTiles();
    }
*/
    public void switchTurns()
    {
        // switch from player one to player to and vice versa
        playerNum += 1;
        // resets count if at the end of the current list of players
        if (playerNum == playerList.Length || !playerList[playerNum].enabled) playerNum = 0;
        curPlayer = playerList[playerNum];
        numPicks++;
        // use this instead of below because of options beyond picking tiles
        if (numPicks == lettersPerRow - 2)
        {
            numPicks = 0;
            curTileGroup++;
            if (curTileGroup == horizontalLayouts.Count)
            {
                foreach(PlayerController player in playerList)
                {
                    if (player.enabled)
                    {
                        gameManager.wordList.Add(player.getLetters());
                    }
                }
                gameManager.loadNextScene();
            }
            horizontalLayouts[curTileGroup].GetComponent<TileHolder>().flipTiles();
        }

/*        if (horizontalLayouts[curTileGroup].GetComponent<TileHolder>().letterScripts.Count == 2)
        {
            curTileGroup++;
            if (curTileGroup == horizontalLayouts.Count)
            {
                curTileGroup = 0;
            }
            horizontalLayouts[curTileGroup].GetComponent<TileHolder>().flipTiles();


        }*/
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
