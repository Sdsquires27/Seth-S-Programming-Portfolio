using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class ButtonSlideScript : MonoBehaviour
{
    public SlideSettingManager slideSettingManager;
    public TextMeshProUGUI text;

    public void changeText()
    {
        text.text = slideSettingManager.curNum.ToString();
    }
}
