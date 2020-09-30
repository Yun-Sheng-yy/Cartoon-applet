// pages/search/index.js
import { request } from "../../request/index.js";
import regeneratorRuntime from '../../lib/runtime/runtime';
Page({

  /**
   * 页面的初始数据
   */
  data: {
    textVal:'',
    dict_list:{}
  },

  handleInput(e){
    // console.log(e)
    this.setData({
      textVal:e.detail.value
    })
    
  },
  handleCancel(){
    const {textVal} = this.data
    this.get_manhua_data(textVal)
  },

  async get_manhua_data(manhua_name){
    const res = await request({url:'/get_title', data:{"name":manhua_name}})
    // 获取到数据进行赋值
    this.setData({
      dict_list:res
    })

    wx.hideLoading();
  },

  handleClick(e){
    const {img, name}=e.currentTarget.dataset
    // console.log(img,name)
    var manhua_data = {
      img:img,
      name:name
    }
    // 4.把数组存入到缓存里面
    wx.setStorageSync('manhua_data', manhua_data);
  }
})