using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class ButtonScript : MonoBehaviour
{ 
    public void sceneLoad(string scene)
    {
        if(scene == "Phase One" && GameManager.instance != null)
        {
            DontDestroyOnLoad(GameManager.instance);
        }
        SceneManager.LoadScene(scene);
    }

    public void quit()
    {
        Application.Quit();
    }

    public void loadEndGame()
    {
        GameManager.instance.loadEndGame();
    }

    public void startLoadNewScene()
    {
        SoundManager.instance.fadeSound();
    }
}
