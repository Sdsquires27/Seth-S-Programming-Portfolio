using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

public class BuySpell : MonoBehaviour, IPointerClickHandler
{
    public int cost;
    public SpellTile spell;

    // Start is called before the first frame update
    void Start()
    {
        
    }
    public void OnPointerClick(PointerEventData eventData)
    {

        if (GameManager.instance.buyTile(cost))
        {
            SpellTile tile = GameManager.createSpell(spell.GetComponent<Image>(), transform.position);
            GameManager.instance.handleTileClick(tile);
        }

    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
