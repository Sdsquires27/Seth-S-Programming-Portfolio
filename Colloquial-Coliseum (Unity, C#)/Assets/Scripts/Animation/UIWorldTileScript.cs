using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using UnityEngine.EventSystems;
using UnityEngine.SceneManagement;
using UnityEngine.Events;
using UnityEngine.UI;


public class UIWorldTileScript : MonoBehaviour, IPointerClickHandler, IPointerEnterHandler, IPointerExitHandler, ISelectHandler
{
    // a class that controls the gray tiles that do not have any affect on the actual game

    // components
    public Animator anim;
    [SerializeField] private TextMeshProUGUI letterText;
    [SerializeField] private Animator letterAnim;
    [SerializeField] private string[] states = new string[2];
    public string curState { get { return states[anim.GetBool("TileFlipped") ? 0 : 1]; } }
    [SerializeField] private string infoText;
    [SerializeField] private bool active = true;
    Selectable selectable;
    public AudioClip sound;


    [Header("Optional")]
    [SerializeField] private bool useFlipped;
    [SerializeField] private UnityEvent flipped;
    [SerializeField] private UnityEvent initialFlipped;

    public bool activated { get { return anim.GetBool("TileFlipped"); } }
    public void OnPointerClick(PointerEventData pointerEventData)
    {

        if (!active) return;
        if (!(anim.GetCurrentAnimatorStateInfo(0).IsName("TileAnimation")))
        {
            // activate the trigger
            anim.SetTrigger("TileFlip");

            // change the value of tile flipped
            anim.SetBool("TileFlipped", !anim.GetBool("TileFlipped"));
            StartCoroutine(changeText(states[anim.GetBool("TileFlipped") ? 0 : 1], .2f));
            if (useFlipped)
            {
                initialFlipped?.Invoke();
                StartCoroutine(functionDelay(.8f));
            }
            letterAnim.SetBool("TileFlipped", !letterAnim.GetBool("TileFlipped"));
        }
    
    }

    public void playSound()
    {
        SoundManager.instance.PlaySound(sound);
    }

    public void setActive(bool active)
    {
        this.active = active;
        GetComponent<Image>().color = active ? Color.white : Color.gray;
    }

    public void OnPointerEnter(PointerEventData pointerEventData)
    {
        Debug.Log("Pointer enter");
        if (!active) return;

        Debug.Log("Active");
        if(infoText != "") InformationPanel.callPanel(infoText, transform.position + new Vector3(0, 100));
        // set the tile touched variable in animators
        anim.SetBool("TileTouched", true);
        letterAnim.SetBool("TileTouched", true);
    }

    public void OnPointerExit(PointerEventData pointerEventData)
    {
        // set the tile touched variable in animator
        if(infoText != "") InformationPanel.dismissPanel();
        anim.SetBool("TileTouched", false);
        letterAnim.SetBool("TileTouched", false);
    }

    public void setReveal(bool revealed)
    {
        if (!active) return;

        // reveal tile function
        anim.SetBool("TileFlipped", revealed);
        letterAnim.SetBool("TileFlipped", revealed);
    }

    private IEnumerator changeText(string text, float time)
    {

        yield return new WaitForSeconds(time);
        letterText.text = text;
    }

    private IEnumerator functionDelay(float time)
    {
        yield return new WaitForSeconds(time);
        flipped.Invoke();
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
        sound = Resources.Load<AudioClip>("Sounds/Hit3");
        letterText.text = states[0];
    }

    public void setValue(bool newValue)
    {
        if (activated != newValue)
        {

            anim.SetBool("TileFlipped", newValue);
            letterAnim.SetBool("TileFlipped", newValue);
            StartCoroutine(changeText(states[anim.GetBool("TileFlipped") ? 0 : 1], .2f));
        }
    }

    public void OnSelect(BaseEventData eventData)
    {
        throw new System.NotImplementedException();
    }
}
