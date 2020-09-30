// pages/detail_img/index.js
import { request } from "../../request/index.js";
import regeneratorRuntime from '../../lib/runtime/runtime';
Page({

  /**
   * 页面的初始数据
   */
  data: {
    manhua_list:[],
    index:'',
    manhua_len:'',
  },

  onShow(){
    // onshow从页面里面获取传进来的参数
    let pages = getCurrentPages();
    let currentPage = pages[pages.length-1];
    let options = currentPage.options;
    // console.log(options)
    // 获取页面参数将数据传过去
    const {url} = options;

    // 获取到缓存
    const manhua_list=wx.getStorageSync('manhua_list')||[];
    let len=manhua_list.length
    console.log(manhua_list)
    // 拿到当前点击进去的索引
    let index = manhua_list.findIndex(v=>v.detail_url===url);
    this.setData({
      manhua_list,
      index,
      manhua_len:len
    })
    console.log(index)
    this.get_manhua_img_detail(url)
    // console.log("hahah"+url)
  },

  // 调用发生请求方法
  async get_manhua_img_detail(url){
    const res = await request({url:'/get_manhua_detail', data:{"url":url}})
    // 获取到数据进行赋值
    this.setData({
      manhua_img_dict_list:res,
    })
    wx.pageScrollTo({
      scrollTop: 0
    })

     // 关闭下拉加载动画
     wx.stopPullDownRefresh();

    //  关闭加载动画
     wx.hideLoading();
  },
  // 获取到索引
  // 下拉index加一,获取上一话数据,并且判断有没有上一话
  onPullDownRefresh(){
    // console.log("触顶事件")

    let index = this.data.index
    const {manhua_list} = this.data
    index --;
    console.log("看看有什么一"+index)
    if(index<0){
      
      wx.showToast({
        title: '没有上一话数据',
      })
      // 没有数据结束上拉加载效果
      wx.stopPullDownRefresh();

      return
    }
    this.setData({
      index
    })

    // 4.通过索引，把选中状态取反
    let url = manhua_list[index].detail_url
    this.get_manhua_img_detail(url)

  },
  // 上拉,触底加载获取下一话数据,判断有没有下一话
  onReachBottom(){
    // console.log("触底")
    let index = this.data.index
    const {manhua_len,manhua_list} = this.data
    
    index ++;
    console.log("看看有什么二"+index,manhua_len)
    if(index>=manhua_len){
      
      wx.showToast({
        title: '没有下一话数据',
      })

      return
    }
    this.setData({
      index  
    })
    // 4.通过索引，拿到下一话的url
    let url = manhua_list[index].detail_url
    this.get_manhua_img_detail(url)
  }


})