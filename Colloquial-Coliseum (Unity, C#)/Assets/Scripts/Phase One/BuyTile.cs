using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using TMPro;

public class BuyTile : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler, IPointerClickHandler
{
    // A tile that can be bought

    // buy tile
    [SerializeField] private Animator letterAnim;
    private Animator anim;
    private TextMeshProUGUI text;
    private Letter letter;
    private int cost;

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

    public void OnPointerClick(PointerEventData eventData)
    {
       
        if (GameManager.instance.buyTile(cost))
        {
            LetterScript letter = GameManager.createLetter(text.text[0], transform.position);
            GameManager.instance.handleTileClick(letter);
        }

    }


    // Start is called before the first frame update
    void Start()
    {
        anim = GetComponent<Animator>();
        text = GetComponentInChildren<TextMeshProUGUI>();
        letter = Resources.Load<Letter>("Letters/" + text.text[0]);
        cost = letter.worth * 100;
        if (cost > 500) cost = 500;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
