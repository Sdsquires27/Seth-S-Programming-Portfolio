using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using TMPro;

public class ActionChoice : MonoBehaviour, IPointerClickHandler, IPointerEnterHandler, IPointerExitHandler, IInfoPanel
{
    LevelScript levelScript;
    Action action;
    public bool selected;
    private bool highlighted;
    private bool canUse { get{ return action.timeRecharging == 0; } }
    [SerializeField] private TextMeshProUGUI text;

    public string description
    {
        get
        {
            return action.description;
        }
    }

    public void OnPointerClick(PointerEventData eventData)
    {
        levelScript.changeSelectedAction(action);
    }

    public void OnPointerEnter(PointerEventData eventData)
    {
        highlighted = true;
    }

    public void OnPointerExit(PointerEventData eventData)
    {
        highlighted = false;
    }

    public void setAction(Action action)
    {
        this.name = action.name;
        this.action = action;
        
    }

    // Start is called before the first frame update
    void Start()
    {
       levelScript = FindObjectOfType<LevelScript>();
    }

    // Update is called once per frame
    void Update()
    {
        GetComponent<Image>().color = Color.white;
        if (canUse)
        {
            text.text = "";
            if (selected)
            {
                GetComponent<Image>().color = Color.red;
                if (highlighted)
                {
                    GetComponent<Image>().color = Color.magenta;
                }

            }
            else if (highlighted)
            {
                GetComponent<Image>().color = Color.gray;
            }
        }
        else
        {
            GetComponent<Image>().color = Color.gray;
            text.text = action.timeRecharging.ToString();
        }
    }
}
