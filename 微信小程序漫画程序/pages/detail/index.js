// pages/detail/index.js
import { request } from "../../request/index.js";
import regeneratorRuntime from '../../lib/runtime/runtime';
Page({

  /**
   * 页面的初始数据
   */
  data: {
    manhua_dict_list:{},
    isCollect:false,
    manhua_data:{},
    url:"",
    user_name:"",
    isFocus:false,
  },
  onShow(){
    // 从缓存里获取数据
    this.get_user_data()
    const manhua_data=wx.getStorageSync('manhua_data')||[];
    this.setData({
      manhua_data,
    })
    // 登陆才显示
    if(this.data.user_name!==undefined){
      this.setData({
        isFocus:true
      })
    }
    

    // onshow从页面里面获取传进来的参数url
    let pages = getCurrentPages();
    let currentPage = pages[pages.length-1];
    let options = currentPage.options;
    // console.log(options)
    // 获取页面参数将数据传过去
    const {url} = options;
    this.setData({url})
    this.get_manhua_detail(url)

    // 检查是否在收藏里面的逻辑
    // 1.获取漫画url，及用户数据
    let user_name = this.data.user_name
    // 2.如果存在数据库，可以调用我的那里的收藏接口，就将标签，收藏标签，置为收藏
    this.get_data(url,user_name)

  },
  get_user_data(){
    // 从缓存里面取数据
    const userinfo=wx.getStorageSync('userinfo');
    this.setData({
      user_name:userinfo.nickName
    })
  },
  // 调用发生请求方法
  async get_manhua_detail(url){
    const res = await request({url:'/get_detail', data:{"url":url}})
    // 把数组存入到缓存里面
    wx.setStorageSync('manhua_list', res.data.data);
    // 获取到数据进行赋值
    this.setData({
      manhua_dict_list:res
    })
    //  关闭加载动画
    wx.hideLoading();
  },

  // 点击收藏
  ShuochangClick(){
    let user_name = this.data.user_name
    if(user_name===undefined){return}
    let isCollect =! this.data.isCollect
    console.log(isCollect)
    if(isCollect){
      console.log("点击收藏加入数据库逻辑")
      // 1.加入获取数据，发送请求将数据加入到数据库
      // 构造需要保存的数据
      let data = {
        "user_name":user_name,
        "manhua_url":this.data.url,
        "manhua_name":this.data.manhua_data.name,
        "manhua_img":this.data.manhua_data.img,
        "type_data":"save_collection"
      }
      console.log(data)
      this.save_manhua_data(data)

    }
    else{
      // console.log("取消收藏了")
      // 取消收藏的逻辑
      const manhua_url = this.data.url
      let user_name1 = user_name
      this.delect_data(manhua_url,user_name1)

    }
    this.setData({
      isCollect
    })
  },
  // 点击收藏或者浏览漫画的时候加入到数据库,
  async save_manhua_data(data){
    const res = await request({url:'/save_collection_historical',method:"POST", data:data})
    console.log(res)
    wx.hideLoading();
    if (data.type_data==="save_collection"){
      if (res.data.errno==="0"){
        wx.showToast({
          title: '收藏成功',
        })
      }
      else{
        wx.showToast({
          title: res.data.errmsg,
        })
      }
    }
  },

  // 获取收藏的全部数据，判断当前的链接是否在数据库里面
  async get_data(is_suochang_url,user_name){
    if(user_name===undefined){return}
    const res = await request({url:"/collection_historical_data",data:{"type":"collection",
    "user_name":user_name,
    "bg":0,
    "be":10000000000000000000}})
    console.log(res)
    // console.log("看看执行没有")
    if(res.data.errno===0){
      // console.log("看看执行没有")
      let index = res.data.data.findIndex(v => v.manhua_url===is_suochang_url)
      console.log(index)
      if (index!==-1){
        // 如果查得到数据
        console.log("看看执行没有")
        this.setData({
          isCollect:true
        })
      }
      wx.hideLoading();
      return
    }
    wx.hideLoading();
  },

  // 取消收藏的逻辑
  async delect_data(manhua_url,user_name){
    const res = await request({url:"/delete_data",method:"DELETE", data:{
      url:manhua_url,
      user_name:user_name,
      type_data:"Collection"
    }})
    wx.hideLoading();
    console.log(res)
    if (res.data.errno==="2")
    {
      wx.showToast({
        title: '取消收藏',
      })
    }
    else{
      wx.showToast({
        title: res.data.errmsg,
      })
    }
  },
  // 绑定点击事件
  save_history(){
    console.log("点击了")
    // 点击的时候加入将浏览历史加入到数据库
    let user_name = this.data.user_name
    if(user_name===undefined){return}
    let data = {
      "user_name":user_name,
      "manhua_url":this.data.url,
      "manhua_name":this.data.manhua_data.name,
      "manhua_img":this.data.manhua_data.img,
      "type_data":"save_historical"
    }
    console.log(data)
    this.save_manhua_data(data)

  }
})