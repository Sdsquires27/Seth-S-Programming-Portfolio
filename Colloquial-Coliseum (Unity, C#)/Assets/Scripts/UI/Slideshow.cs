using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using TMPro;

public class Slideshow : MonoBehaviour
{
    public string[] shownText;
    public TextMeshProUGUI text;
    public TextMeshProUGUI text2;

    private int index;
    public string nextScene;

    // Start is called before the first frame update
    void Start()
    {
        text.text = shownText[0].Replace("\\n", "\n");
        text2.text = text.text;
        index = 0;


    }

    public void nextInitial()
    {
        index++;
        if (shownText.Length > index)
        {
            text.text = shownText[index].Replace("\\n", "\n");
            text2.GetComponent<Animator>().SetTrigger("SlideAway");
            text.GetComponent<Animator>().SetTrigger("SlideIn");
        }
    }

    public void next()
    {
        text2.text = text.text;
        if (shownText.Length <= index)
        {
            SceneManager.LoadScene(nextScene);
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
