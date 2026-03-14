using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using UnityEngine;
using TMPro;

public class GameModeManager : MonoBehaviour
{
    public string resourcesLocation;
    TextAsset premadeFile;
    public string folderName;
    public string fileName;
    public GameObject presetButton;
    BasicSaveData loadedData;
    [SerializeField] private GameObject nameEntryPanel;



    private void Start()
    {
        nameEntryPanel.SetActive(false);
        loadedData = SaveLoad<BasicSaveData>.Load(folderName, fileName) ?? new BasicSaveData();
        if(loadedData.stringData.Count == 0)
        {
            premadeFile = Resources.Load<TextAsset>(resourcesLocation);
            loadedData.stringData = new List<string>(premadeFile.text.Split('\n'));
            Debug.Log("No data in folder");
        }

        for(int i = 0; i < loadedData.stringData.Count / 7; i++)
        {
            GameObject x = Instantiate(presetButton, this.transform);
            x.GetComponentInChildren<TextMeshProUGUI>().text = loadedData.stringData[i * 7];
            string[] settings = new string[6];
            for(int j = 1; j < 7; j++)
            {
                settings[j - 1] = loadedData.stringData[j + (i * 7)];
            
            }
            x.GetComponent<PresetButton>().instantiate(settings);
        }

        SaveLoad<BasicSaveData>.Save(loadedData, folderName, fileName);

      
    }

    public void textChangedHandler(TMP_InputField text)
    {
        text.text = text.text.ToUpper();
        text.text = GameManager.RemoveSpecialCharacters(text.text); 
    }

    public void newSettingPanel()
    {
        bool noDuplicates = true;
        foreach(PresetButton button in GetComponentsInChildren<PresetButton>())
        {
            noDuplicates = button.checkSettings() ? false : noDuplicates;
        }
        nameEntryPanel.SetActive(noDuplicates);

    }

    public void goBack()
    {
        nameEntryPanel.SetActive(false);
    }

    public void newSetting(TextMeshProUGUI text)
    {
        List<string> curSettings = GameManager.instance.curSettings();
        curSettings.Insert(0, text.text.Remove(4));
        loadedData.stringData.AddRange(curSettings);
        nameEntryPanel.SetActive(false);
        SaveLoad<BasicSaveData>.Save(loadedData, folderName, fileName);
        GameObject x = Instantiate(presetButton, this.transform);
        x.GetComponentInChildren<TextMeshProUGUI>().text = curSettings[0];
        string[] settings = new string[5];
        for (int j = 1; j < 6; j++)
        {
            settings[j - 1] = curSettings[j];

        }
        x.GetComponent<PresetButton>().instantiate(settings);
    }
}

[System.Serializable]
public class BasicSaveData
{
    public List<string> stringData;

    public BasicSaveData()
    {
        stringData = new List<string>();
    }

}

[System.Serializable]
public class DoubleList
{
    public List<string> scores;
    public List<string> names;

    public DoubleList()
    {
        names = new List<string>();
        scores = new List<string>();
    }

}

