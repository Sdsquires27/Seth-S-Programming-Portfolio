using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
using UnityEngine.InputSystem;
using UnityEngine.Audio;

public class GameSettings : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler, IPointerClickHandler
{
    // components
    public static GameSettings instance;
    public GameObject settingsPanel;
    private Image image;
    public AudioMixer audioMixer;
    public UIWorldTileScript infoBarTile;
    public bool infoBarAppears = true;

    public void OnPointerEnter(PointerEventData eventData)
    {
        image.color = Color.white;
    }

    public void SetSound(float soundLevel)
    {
        audioMixer.SetFloat("musicVol", soundLevel);

    }
    public void SetSound2(float soundLevel)
    {
        audioMixer.SetFloat("sfxVol", soundLevel);
    }

    public void OnPointerExit(PointerEventData eventData)
    {
        image.color = new Color(1, 1, 1, .5f);
    }
    public void OnPointerClick(PointerEventData eventData)
    {
        settingsPanel.SetActive(true);
        image.enabled = false;
    }
    public void OnEscapePress(InputAction.CallbackContext context)
    {
        Application.Quit();
    }

    public void OnSceneLoaded(Scene scene, LoadSceneMode loadSceneMode)
    {
        Close();
    }

    public void Close()
    {
        settingsPanel.SetActive(false);
        image.enabled = true;
    }

    // Start is called before the first frame update
    void Start()
    {
        if (instance == null) instance = this;
        else Destroy(transform.parent.gameObject);
        DontDestroyOnLoad(transform.parent.gameObject);

        image = GetComponent<Image>();
        settingsPanel.SetActive(false);
        SceneManager.sceneLoaded += OnSceneLoaded;
    }

   

    // Update is called once per frame
    void Update()
    {
        if (infoBarTile.isActiveAndEnabled)
        {
            infoBarAppears = infoBarTile.activated;
        }
    }
}
