using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using UnityEngine.InputSystem;
using UnityEngine.SceneManagement;

public class InformationPanel : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI text;
    private static InformationPanel instance;

    

    // Start is called before the first frame update
    void Start()
    {
        if (instance == null)
        {
            instance = this;
        }
        else
        {
            Destroy(this.gameObject);
        }
        gameObject.SetActive(false);

    }

    // Update is called once per frame
    void Update()
    {

    }

    public static void callPanel(string text)
    {
        instance.text.text = text;
        instance.gameObject.SetActive(true);
    }
    public static void callPanel(string text, Vector2 pos)
    {
        if (GameSettings.instance.infoBarAppears || SceneManager.GetActiveScene().name == "ModeSelect")
        {
            instance.text.text = text;

            if ((pos.y + instance.GetComponent<RectTransform>().rect.height) > Screen.height)
            {
                pos = new Vector3(pos.x + 300, Screen.height - instance.GetComponent<RectTransform>().rect.height);
            }

            instance.transform.position = pos;


            instance.gameObject.SetActive(true);
        }

    }
    public static void dismissPanel()
    {
        instance.gameObject.SetActive(false);
    }

}


