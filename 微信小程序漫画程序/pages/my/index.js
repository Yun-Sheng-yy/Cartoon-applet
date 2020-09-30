// pages/my/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    isFocus:false,
    user_name:""
  },

  handleGetUserInfo(e){
    console.log(e)
    // 获取用户信息
    const {userInfo} = e.detail;
    // 保存到缓存里面
    wx.setStorageSync('userinfo', userInfo);
    this.get_data()

    if(this.data.user_name!==undefined){
      this.setData({
        isFocus:true
      })
  }
  },
  get_data(){
    // 从缓存里面取数据
    const userinfo=wx.getStorageSync('userinfo');
    this.setData({
      userinfo,
      user_name:userinfo.nickName
    })
  },
  onShow(){
    this.get_data()
    // 登陆显示底部
    if(this.data.user_name!==undefined){
        this.setData({
          isFocus:true
        })
    }
    
  }

  
})