export const request=(params)=>{

  // 显示加载中效果
  wx.showLoading({
    title: '加载中',
    // mask朦胧效果
    mask:true
  });
  // 定义公共的url,接口改的时候可以轻易的改变
  const baseUrl = "http://127.0.0.1:5000/api/v1.0"
  return new Promise((resolve, reject)=>{
    wx.request({
      ...params,
      url:baseUrl+params.url,
      success:(result)=>{
        resolve(result);
      },
      fail:(err)=>{
        reject(err);
      }
    });
  })
}