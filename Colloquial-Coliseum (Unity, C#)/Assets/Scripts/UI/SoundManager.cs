using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class SoundManager : MonoBehaviour
{
    public static SoundManager instance;
    public List<string> sceneNames;
    public AudioClip[] sounds;
    public AudioSource usedAudio;
    public AudioSource sfxAudio;

    private void Start()
    {
        if(instance == null)
        {
            instance = this;
        }
        else
        {
            Destroy(this.gameObject);
        }
        SceneManager.sceneLoaded += onSceneLoaded;
        DontDestroyOnLoad(this.gameObject);
        
    }


    public void PlaySound(AudioClip clip)
    {
       sfxAudio.clip = clip;
        sfxAudio.Play();
    }

    public void fadeSound()
    {
        StartCoroutine(FadeAudioSource.StartFade(usedAudio, .8f, 0));
    }

    public void onSceneLoaded(Scene scene, LoadSceneMode loadSceneMode)
    {

        AudioClip clip = sounds[sceneNames.IndexOf(scene.name)];
        if (clip != usedAudio.clip)
        {
            usedAudio.clip = clip;
            usedAudio.Play();
            
        }
        StartCoroutine(FadeAudioSource.StartFade(usedAudio, .8f, 1));
    }


}
