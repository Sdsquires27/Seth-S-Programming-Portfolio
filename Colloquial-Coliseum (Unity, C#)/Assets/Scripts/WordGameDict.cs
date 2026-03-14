using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using System.Linq;

public class WordGameDict {
	// In C# using a HashSet is an O(1) operation. It's a dictionary without the keys!
	private HashSet<string> words = new HashSet<string>();

	private TextAsset dictText;

	
	public void InitializeDictionary(string filename){
        dictText = (TextAsset)Resources.Load(filename, typeof(TextAsset));
        var text = dictText.text;

        foreach (string s in text.Split('\n'))
        {
            words.Add(s);
        }

	}

	public void InitializeDictionary()
	{
		dictText = (TextAsset)Resources.Load("ospd", typeof(TextAsset));
		var text = dictText.text;

		foreach (string s in text.Split('\n'))
		{
			words.Add(s.TrimEnd());

		}

	}


	public bool CheckWord(string word, int minLength){
		if (word.Length < minLength){
			return false;
		}
		
		if(word.Contains(" "))
        {
			bool wordValid = false;
			Letter[] letters = Resources.LoadAll<Letter>("Resources/Letters");
			foreach(Letter letter in letters)
            {
				string tempWord = word.Replace(" ", letter.character.ToString());
                if (words.Contains(word))
				{
					wordValid = true;
                }
            }
			return wordValid;

        }
        else
        {
			return (words.Contains(word));

		}
	}
}
