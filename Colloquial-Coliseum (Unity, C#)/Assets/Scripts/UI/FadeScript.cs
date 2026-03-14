using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class FadeScript : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        Destroy(gameObject, 1.5f);
    }

    private void Update()
    {
        GetComponent<Image>().CrossFadeAlpha(0, 1f, false);
        GetComponentInChildren<TextMeshProUGUI>().CrossFadeAlpha(0, 1f, false);
    }

/*    public IEnumerator fade(float seconds)
    {
        float curTime = Time.timeSinceLevelLoad;
        float targetTime = curTime + seconds;
        while(targetTime > Time.timeSinceLevelLoad)
        {
            GetComponent<Image>().CrossFadeAlpha
            yield return new WaitForEndOfFrame();
        }
    }*/
}
