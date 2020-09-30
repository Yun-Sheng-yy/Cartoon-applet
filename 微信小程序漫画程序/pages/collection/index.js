// pages/collection/index.js
import { request } from "../../request/index.js";
import regeneratorRuntime from '../../lib/runtime/runtime';
Page({

  /**
   * 页面的初始数据
   */
  data: {
    bg:0,
    be:10,
    manhua_data:[],
    isshow:false,
    user_name:""
  },
  onLoad(){  
    // 页面加载的时候判断,登陆了没有
    this.get_user_info()
    // 页面加载的时候，带上用户名，查找的类型，开始的数据 结束的数据,数据回来的时候进行数据拼接
    
    let user_name = this.data.user_name
    this.get_data(user_name)
    
    
  },
  // 获取用户名字
  get_user_info(){
    const userinfo=wx.getStorageSync('userinfo');
    this.setData({
      user_name:userinfo.nickName
    })
  },

  async get_data(user_name){
    if (user_name===undefined){return}
    const res = await request({url:"/collection_historical_data",data:{"type":"collection",
    "user_name":user_name,
    "bg":this.data.bg,
    "be":this.data.be}})
    console.log(res)
    
    if(res.data.errno==="4002"){
      console.log("到底了")
      wx.showToast({
        title: '没有数据:)',
        icon: 'none'
      })
      wx.hideLoading();
      return
    }
    this.setData({
      // 拼接数组，将当前的数据解构，在和新的数据拼接，一开始为空的数组为空不影响
      // [...this.data.goodsList,...res.goods]
      manhua_data:[...this.data.manhua_data,...res.data.data]
    })
    wx.hideLoading();
  },

  // 触底事件
  onReachBottom(){
    // 要通过状态码来判断数据存不存在
    // 将bg 加20，be 加20
    if (this.data.user_name!==undefined){
      console.log("触底了")
      let bg = this.data.bg += 10
      let be = this.data.be += 10
      this.setData({
        bg:bg,
        be:be
      })
      let user_name = this.data.user_name
      this.get_data(user_name)
    }
    return
    

  },

  // 绑定链接的点击事件
  handleClick(e){
    const {img, name}=e.currentTarget.dataset
    // console.log(img,name)
    var manhua_data = {
      img:img,
      name:name
    }
    // 4.把数组存入到缓存里面
    wx.setStorageSync('manhua_data', manhua_data);

  },

  // 取消收藏的逻辑处理
  quxiaoclick(e){
    console.log("点击了取消")
    // 点击取消收藏按钮要做的事情
    // 获取到点击的url，可以通过索引，
    // 把url和用户数据发送到写好的接口

    let {manhua_data} = this.data

    console.log(e.currentTarget.dataset.index)
    // 1.获取点击的索引
    const {index} = e.currentTarget.dataset
    // 2.通过索引找到列表的数据
    // 拿到删除的url
    const manhua_url = manhua_data[index].manhua_url
    console.log(manhua_url)
    manhua_data.splice(index,1)
    // 3.删除数据库里面的数据
    let user_name = this.data.user_name

    this.delect_data(manhua_url,user_name)
    // console.log(res)
    this.setData({manhua_data})
    
  },

  // 删除数据的请求
  async delect_data(manhua_url,user_name){
    if (user_name===undefined){return}
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
  }



})