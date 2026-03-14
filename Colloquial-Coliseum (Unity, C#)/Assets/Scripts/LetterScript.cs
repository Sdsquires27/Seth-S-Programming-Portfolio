using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class LetterScript : MonoBehaviour
{
    [System.NonSerialized] public Letter letter;
    private WordTileScript wordTile;
    [System.NonSerialized] public GameManager gameManager;
    private bool revealed = false;
    [System.NonSerialized] public TileHolder tileHolder;
    [SerializeField] private LetterFollow letterFollowPrefab;
    private LetterFollow letterFollow;

    public void handleTileClick()
    {
        if (revealed) gameManager.handleTileClick(this);
    }

    // Start is called before the first frame update
    void Start()
    {

    }

    public void flip()
    {
        revealed = !revealed;
    }
    public void hide()
    {
        revealed = false;
    }
    public void show()
    {
        revealed = true;
    }

    private void OnDestroy()
    {
        Destroy(letterFollow.gameObject);
    }

    public void initialize(GameManager controller, TileHolder holder, bool teleport = false)
    {
        // Set what is holding the tile
        tileHolder = holder;
        // Set the game Manager
        gameManager = controller;
        // Create the letter follow
        letterFollow = Instantiate(letterFollowPrefab, gameManager.canvas.transform);

        // set up the letter follow
        letterFollow.toFollow = transform;
        wordTile = letterFollow.wordTile;
        wordTile.initialize(letter, this);
        letterFollow.transform.position = transform.position;
        if (teleport) letterFollow.teleport();
    }

    // Update is called once per frame
    void Update()
    {
        wordTile.setReveal(!revealed);
    }
}
