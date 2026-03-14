using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TileObject : MonoBehaviour
{
    public Unit unit;
    public int currentRange;
    public bool canAttack;
    public PlayerController playerController;
    public Sprite sprite;
    public Action action { get { return (actionIndex != -1) ? actions[actionIndex] : null; } }
    public int attackRange;
    public bool isAoe { get { return (action == null) ? false : action.isAoe; } }
    public bool targetsEnemy { get { return (action == null) ? false : action.targetsEnemy; } }

    public Action[] actions;
    public int actionIndex;
    int tempDefense;
    public int thorns;
    public int hp;


    public int aoeSize()
    {
        int size = 0;

        size = action.size;

        return size;
    }

    // Start is called before the first frame update
    void Start()
    {
        hp = unit.hpMax;
        GetComponent<SpriteRenderer>().sprite = unit.sprite;
        GetComponent<SpriteRenderer>().color = playerController.color;
        Action attack = new Action.Attack(unit, this);
        actions = new Action[unit.spells.Count + 1];
        for(int i = 0; i < unit.spells.Count; i++) // starts at 1 because 0 is already taken by the attack action
        {
            actions[i+1] = Resources.Load<Action>("Spells/"+unit.spells[i].name);
        }
        actions[0] = attack;
        setAction(attack);
    }

    public void startTurn()
    {
        foreach(Action action in actions)
        {
            action.reduceChargeTime();
        }

        unit.armor -= tempDefense;
        tempDefense = 0;
        thorns = 0;

        currentRange = unit.moveSpeed;
        canAttack = true;
        setAction(actions[0]);
    }

    public void deactivate()
    {
        canAttack = false;
        if (!unit.moveAfterAttack)
        {
            currentRange = 0;

        }
        attackRange = 0;
    }

    public void useAction(Vector3Int tileAffected, PlayerController curPlayer, TileObject objectAffected)
    {
        if (action.isAoe)
        {
            Debug.Log("Used AoE action");
            action.use(tileAffected, curPlayer);
        }
        else
        {
            action.use(objectAffected, curPlayer);
        }

    }

    public void giveDefense(int defense, int damage = 0)
    {
        tempDefense = defense;
        unit.armor += defense;
        thorns += damage;
        
    }

    public void setAction(Action action)
    {
        if(action != null)
        {
            attackRange = action.range;
            for (int i = 0; i < actions.Length; i++)
            {
                if (actions[i] == action)
                {
                    actionIndex = i;
                }

            }
        }
        else
        {
            attackRange = 0;
            actionIndex = -1;
        }

    }

    public void takeDamage(int damage, PlayerController attacker)
    {
        hp -= damage;

        if (hp <= 0)
        {
            GameManager.giveScore(attacker, unit.word.Length * 200);
            gameObject.SetActive(false);
        }
    }

    public void heal(int amount)
    {
        hp += amount;
        if(hp > unit.hpMax)
        {
            hp = unit.hpMax;
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
