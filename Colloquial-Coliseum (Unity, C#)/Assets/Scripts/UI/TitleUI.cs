using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using System.Linq;
using System;

public class TitleUI : MonoBehaviour
{
    public WordTileHandler word1;
    public WordTileHandler word2;

    public TextMeshProUGUI text;

    public string[] keywords;
    public string[] phrases;

    private void Update()
    {
        string word = word1.word + word2.word;
        if (keywords.Contains(word))
        {
            text.text = phrases[Array.IndexOf(keywords, word)];
        }
        else
        {
            text.text = "";
        }
    }
}
