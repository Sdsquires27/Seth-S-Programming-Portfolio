using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using UnityEngine.UI;

public class UnitCreator : MonoBehaviour
{
    [System.NonSerialized] public List<Unit> units = new List<Unit>(); // list of all units
    public Unit unit; // current unit
    private int index = 0;
    [SerializeField] private TextMeshProUGUI text;
    [SerializeField] private TextMeshProUGUI worthText;
    private TileHolder tileHolder;
    [SerializeField] private UIWorldTileScript endTurnTile;
    [SerializeField] private GameObject statsBar;
    [SerializeField] private GameObject indexBar;
    [SerializeField] private GameObject spellHolderTile;
    [SerializeField] private GameObject spellPlaceholder;
    GameObject spellHolder;

    // Start is called before the first frame update
    void Start()
    {
        tileHolder = GameObject.FindGameObjectWithTag("UnitSpells").GetComponent<TileHolder>();
        spellHolder = GameObject.FindGameObjectWithTag("SpellHolders");
        GameManager.onTurnSwitched += onTurnSwitched;
        endTurnTile.setActive(false);
        gameObject.SetActive(false);
        statsBar.SetActive(false);

    }

    private void OnDisable()
    {
        GameManager.onTurnSwitched -= onTurnSwitched;
    }

    public void onTurnSwitched()
    {
        endTurnTile.setActive(false);
        gameObject.SetActive(false);
        statsBar.SetActive(false);
        unit = null;
    }

    public void addSpell(SpellTile spell)
    {
        if (unit != null)
        {
            if (unit.spellSlots > unit.spellTiles.Count)
            {
                spell.spellHolder.removeTile(spell);
                spell.transform.SetParent(tileHolder.transform);
                unit.spellTiles.Add(spell);

                bool foundHolder = false;
                foreach (Transform x in tileHolder.transform)
                {
                    if (!foundHolder)
                    {
                        if (x.tag == "SpellPlaceholder")
                        {
                            Destroy(x.gameObject);
                            foundHolder = true;
                        }
                    }

                }
            }
        }

    }

    public void clearUnits()
    {
        foreach (SpellTile spell in unit.spellTiles)
        {
            spell.gameObject.SetActive(false);
        }
        units.Clear();
        unit = null;
    }

    public bool canEndTurn()
    {
        if (units.Count == 0) return false;
        bool canEnd = true;
        foreach(Unit unit in units)
        {
            bool needSpells = unit.spellSlots != unit.spellTiles.Count;
            if ((unit.worth != 0) || (needSpells && !GameManager.instance.spellHolder.hasNoTiles()))
            {

                canEnd = false;
            }
        
        }

        return canEnd;
    }

    public void removeSpell(SpellTile spell)
    {
        Instantiate(spellPlaceholder, tileHolder.transform);

        unit.spellTiles.Remove(spell);
    }

    public void addUnit(Unit newUnit)
    {
        gameObject.SetActive(true);
        statsBar.SetActive(true);
        units.Add(newUnit);
        if(unit != null)
        {
            foreach (SpellTile spell in unit.spellTiles)
            {
                spell.gameObject.SetActive(false);
            }
        }

        index = units.Count - 1;
        unit = units[index];
        showSpells();
        foreach (SpellTile spell in unit.spellTiles)
        {
            spell.gameObject.SetActive(true);
        }
        indexBar.SetActive(units.Count > 1 ? true : false); // set the bar that allows you to select units to active if there are units to cycle through.
    }

    private void showSpells()
    {
        foreach(Transform t in spellHolder.transform)
        {
            Destroy(t.gameObject);
        }
        foreach (Transform t in tileHolder.transform)
        {
            if(t.tag == "SpellPlaceholder")
            Destroy(t.gameObject);
        }
        for (int i = 0; i < unit.spellSlots; i++)
        {
            Instantiate(spellHolderTile, spellHolder.transform);

        }
        for (int i = 0; i < unit.spellSlots - unit.spellTiles.Count; i++)
        {
            Instantiate(spellPlaceholder, tileHolder.transform);
        }

    }

    public void changeIndex(bool up)
    {
        index += up ? 1 : -1;
        if (index == units.Count)
        {
            index = 0;
        }
        else if (index == -1)
        {
            index = units.Count - 1;
        }
        foreach (SpellTile spell in unit.spellTiles)
        {
            spell.gameObject.SetActive(false);
        }
        unit = units[index];
        showSpells();
        foreach (SpellTile spell in unit.spellTiles)
        {
            spell.gameObject.SetActive(true);
        }
    }

    public void upStat(string stat)
    {
        if (unit.worth > 0)
        {
            unit.worth--;
            if (stat == "HP")
            {
                unit.hpMax+=2;
            }
            else if (stat == "DMG")
            {
                unit.dmg++;
            }
            else if (stat == "SPD")
            {
                unit.moveSpeed++;
            }
            else if (stat == "ARMOR")
            {
                unit.armor++;
            }
            else if (stat == "PRC")
            {
                unit.piercing++;
            }
        }

    }

    public void downStat(string stat)
    {
        if (stat == "HP" && unit.hpMax > unit.hpMin)
        {
            unit.hpMax-= 2;
            unit.worth++;
        }
        else if (stat == "DMG" && unit.dmg > unit.dmgMin)
        {
            unit.dmg--;
            unit.worth++;
        }
        else if (stat == "SPD" && unit.moveSpeed > unit.moveSpeedMin)
        {
            unit.moveSpeed--;
            unit.worth++;
        }
        else if (stat == "ARMOR" && unit.armor > unit.armorMin)
        {
            unit.armor--;
            unit.worth++;
        }
        else if (stat == "PRC" && unit.piercing > unit.pierceMin)
        {
            unit.piercing--;
            unit.worth++;
        }

    }

    // Update is called once per frame
    void Update()
    {
        if (unit != null)
        {
            text.text = unit.word;
            worthText.text = unit.worth.ToString();
            GetComponent<Image>().sprite = unit.sprite;
        }
        else
        {
            text.text = "";
        }
        if (canEndTurn())
        {
            endTurnTile.setActive(true);
        }
        else
        {
            endTurnTile.setActive(false);
        }
    }
}
