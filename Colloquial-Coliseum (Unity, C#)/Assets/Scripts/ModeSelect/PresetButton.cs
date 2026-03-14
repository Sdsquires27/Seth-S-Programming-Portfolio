using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using TMPro;

public class PresetButton : MonoBehaviour, IPointerClickHandler, IPointerEnterHandler, IPointerExitHandler
{
    [SerializeField] private TextMeshProUGUI letterText;
    [SerializeField] private string[] settings;
    public Animator anim;
    private string text;
    public Animator letterAnim;
    public AudioClip sound;


    public void instantiate(string[] settings)
    {
        this.settings = settings;
    }

    public void OnPointerClick(PointerEventData pointerEventData)
    {

        if (!anim.GetBool("TileFlipped"))
        {

            GameManager.instance.newSettings(settings);
        }

    }

    public void playSound()
    {
        SoundManager.instance.PlaySound(sound);
    }

    private IEnumerator changeText(string text, float time)
    {
        yield return new WaitForSeconds(time);
        letterText.text = text;
    }

    public void OnPointerEnter(PointerEventData pointerEventData)
    {
        InformationPanel.callPanel(settingsToString(), transform.position + new Vector3(0, 100));
        // set the tile touched variable in animators
        anim.SetBool("TileTouched", true);
        letterAnim.SetBool("TileTouched", true);
    }

    private string settingsToString()
    {
        string ret = text + "\n";

        ret += "TYPE: " + (settings[0].Trim() == "true" ? "DRAFTING" : "BUY") + "\n";
        ret += "ROUNDS: " +settings[1] + "\n";
        ret += "TILE COUNT: " + settings[5] + "\n";
        if (settings[0].Trim() != "true")
        {
            ret += "POINT GAIN: " + (settings[2].Trim() == "true" ? "SCORE" : "EQUAL") + "\n";
            ret += "ROUND BONUS: " + settings[3] + "\n";
            ret += "HANDICAP: " + (settings[4].Trim() == "true" ? "NO" : "YES") + "\n";
        }

        return ret;
    }

    public void OnPointerExit(PointerEventData pointerEventData)
    {
        InformationPanel.dismissPanel();
        // set the tile touched variable in animator
        anim.SetBool("TileTouched", false);
        letterAnim.SetBool("TileTouched", false);
    }



    public void Update()
    {
        if (checkSettings())
        {
            if (!anim.GetBool("TileFlipped"))
            {
                if (anim.GetBool("TileTouched"))
                {
                    anim.SetTrigger("TileFlip");
                }
                anim.SetBool("TileFlipped", true);
                StartCoroutine(changeText("", .2f));
                letterAnim.SetBool("TileFlipped", true);
            }
        }
        else
        {
            if (anim.GetBool("TileFlipped"))
            {
                anim.SetBool("TileFlipped", false);
                StartCoroutine(changeText(text, .2f));
                letterAnim.SetBool("TileFlipped", false);
            }
        }
    }

    public void Start()
    {
        text = letterText.text;
        sound = Resources.Load<AudioClip>("Sounds/Hit3");

    }

    public bool checkSettings()
    {
        bool same = true;
        for(int i = 0; i < settings.Length; i++)
        {
            string setting = settings[i];
            string gameSetting = GameManager.instance.curSettings()[i];
            
            if (setting.Trim().ToLower() != "null" && setting.Trim().ToLower() != gameSetting.ToLower()) same = false;
        }

        return same;
    
    }
}
