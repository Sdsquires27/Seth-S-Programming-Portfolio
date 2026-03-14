using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using TMPro;

public class WordTileScript : MonoBehaviour, IPointerClickHandler, IPointerEnterHandler, IPointerExitHandler
{
    private Animator anim;
    [SerializeField] private Animator letterAnim;
    [SerializeField] private TextMeshProUGUI letterText;
    [SerializeField] private TextMeshProUGUI worthText;
    public Letter letter;
    private LetterScript letterScript;
    private GameManager gameManager;
    public AudioClip sound;

    public void OnPointerClick(PointerEventData pointerEventData)
    {
        if (letterScript == null)
        {
            if (!(anim.GetCurrentAnimatorStateInfo(0).IsName("TileAnimation")))
            {
                // activate the trigger
                anim.SetTrigger("TileFlip");

                // change the value of tile flipped
                anim.SetBool("TileFlipped", !anim.GetBool("TileFlipped"));
                letterAnim.SetBool("TileFlipped", !letterAnim.GetBool("TileFlipped"));
            }
        }
        else
        {
            letterScript.handleTileClick();
        }
    }

    public void playSound()
    {
        SoundManager.instance.PlaySound(sound);
    }

    public void OnPointerEnter(PointerEventData pointerEventData)
    {
        // set the tile touched variable in animators
        anim.SetBool("TileTouched", true);
        letterAnim.SetBool("TileTouched", true);
    }

    public void OnPointerExit(PointerEventData pointerEventData)
    {
        // set the tile touched variable in animator
        anim.SetBool("TileTouched", false);
        letterAnim.SetBool("TileTouched", false);
    }

    public void setReveal(bool revealed)
    {
        // reveal tile function
        anim.SetBool("TileFlipped", revealed);
        letterAnim.SetBool("TileFlipped", revealed);
    }

    public void revealTile()
    {
        // reveal tile function
        anim.SetBool("TileFlipped", false);
        letterAnim.SetBool("TileFlipped", false);
    }

    public void hideTile()
    {
        // hide tile function
        anim.SetBool("TileFlipped", true);
        letterAnim.SetBool("TileFlipped", true);
    }

    // Start is called before the first frame update
    void Start()
    {
        // get the current animation
        anim = GetComponent<Animator>();
        gameManager = FindObjectOfType<GameManager>();
        sound = Resources.Load<AudioClip>("Sounds/Hit3");
    }

    public void initialize(Letter newLetter)
    {
        letter = newLetter;
        // set the letter text and worth text
        letterText.text = letter.character.ToString();
        worthText.text = letter.worth.ToString();
    }

    public void initialize(Letter newLetter, LetterScript newLetterScript)
    {
        letter = newLetter;
        letterScript = newLetterScript;
        // set the letter text and worth text

        // TODO: figure out how to make a wild character
        letterText.text = letter.character.ToString();
        worthText.text = letter.worth.ToString();

    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
