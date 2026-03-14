using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using UnityEngine.EventSystems;

public class SpellTile : MonoBehaviour, IPointerClickHandler, IInfoPanel
{
    private Image image;
    private Sprite sprite;
    [System.NonSerialized] public TileHolder spellHolder;
    private LetterFollow letterFollow;
    private GameManager gameManager;
    public LetterFollow letterFollowPrefab;
    
    public string description
    {
        get
        {
            if(SceneManager.GetActiveScene().name == "Phase One")
            {

            }
            if (SceneManager.GetActiveScene().name == "Phase Two")
            {

            }
            return GameManager.spellDescription(sprite.name);
        }
    }

    public void OnPointerClick(PointerEventData pointerEventData)
    {
        gameManager.handleTileClick(this);
    }

    public string packName()
    {
        // take the name, remove the "Spell" from the end and return the result.
        string tempName = sprite.name;
        tempName = tempName.Remove(tempName.Length - 5);
        return tempName;
    }

    public void initialize(GameManager controller, TileHolder holder, Sprite newSprite)
    {
        holder?.addTile(this);
        spellHolder = holder;
        sprite = newSprite;
        gameManager = controller;
        letterFollow = Instantiate(letterFollowPrefab, gameManager.canvas.transform);
        letterFollow.toFollow = transform;
        image = letterFollow.GetComponent<Image>();
        image.sprite = sprite;
        letterFollow.transform.position = Vector3.zero;
    }

    private void OnDisable()
    {
        letterFollow.gameObject.SetActive(false);
    }

    private void OnEnable()
    {
        if (letterFollow != null)
        {
            letterFollow.gameObject.SetActive(true);
        }
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
