using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SlideSettingManager : MonoBehaviour
{
    // settings for numbers & range of numbers
    [System.NonSerialized] public int curNum;
    public int maxNum;
    public int minNum;
    public int increment;
    public Animator anim;

    public void Start()
    {
        curNum = minNum;
    }

    public void increaseNum()
    {
        if (anim.GetCurrentAnimatorStateInfo(0).IsName("tileSlide"))
        {
            anim.SetTrigger("MoveRight");
            curNum += increment;
            if (curNum > maxNum)
            {
                curNum = minNum;
            }
        }

    }
    public void decreaseNum()
    {
        if (anim.GetCurrentAnimatorStateInfo(0).IsName("tileSlide"))
        {
            anim.SetTrigger("MoveLeft");
            curNum -= increment;
            if (curNum < minNum)
            {
                curNum = maxNum;
            }
        }

    }

    public void setNum(int num)
    {
        if (anim.GetCurrentAnimatorStateInfo(0).IsName("tileSlide"))
        {
            if (num > curNum)
            {
                anim.SetTrigger("MoveRight");

            }
            else if(num < curNum)
            {
                anim.SetTrigger("MoveLeft");
            }
            curNum = num;

        }
    }
}
