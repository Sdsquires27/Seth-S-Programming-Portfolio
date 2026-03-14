using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

public class InformationIcon : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler
{
    [SerializeField] private string description;
    [SerializeField] private int yOffset;
    [SerializeField] private int xOffset;

    public void Start()
    {
        if(description == "")
        {
            description = GetComponent<IInfoPanel>().description;
        }
    }

    public void OnPointerEnter(PointerEventData eventData)
    {
            InformationPanel.callPanel(description, new Vector2(transform.position.x + xOffset, transform.position.y + yOffset));
    }

    public void OnPointerExit(PointerEventData eventData)
    {

            InformationPanel.dismissPanel();
    }
}

public interface IInfoPanel
{
    public string description { get; }
}