# 前言
在做毕设的过程总会遇到很多各种各样的问题，有些还会重复出现。感觉是时候，专门写一篇笔记来记录一下了。
之前用evernote记录过一点，但总感觉非常不方便，感觉跟项目比较分离。最近刚好在学习markdown以及打算使用github写博，那就直接利用这个机会，既能掌握markdown又能记录问题。
其实问题的记录很重要，不仅是为了防止下次重复出错以及即使重复出错了也有记录可寻，同时有利于整理整个毕设开发过程，用于日后面试问到“你在项目中遇到什么问题”，“什么问题是最难的啊”

# Flask方面
### blueprint
- 在蓝图中使用`redirect(url_for(xxxx))`进行重定向,`xxxx = 蓝图名.函数名`否则没法实现直接跳转

### 异步
通常情况下一个[异步过程](http://www.cnblogs.com/manxisuo/p/5138050.html)：主线程发起一个异步请求，相应的工作线程接收请求并告知主线程已收到(异步函数返回)；主线程可以继续执行后面的代码，同时工作线程执行异步任务；工作线程完成工作后，通知主线程；主线程收到通知后，执行一定的动作(调用回调函数)。

一个异步函数格式一般是
`func(args...,callbackFn..)`,args是参数，而callbackFn是回调函数，比如
```javascript
//异步请求
$.ajax({
    type: '', //参数
    url: '', //参数
	...
    success: function(){}  //回调函数
	...
});
```
而关于工作线程在执行完异步任务后如何通知主线程呢？
答案是利用消息队列和事件循环（主线程重复从消息队列中取指令，执行的过程）
通知主线程的完整描述是
```
工作线程执行完异步任务后把对应的回调函数封装成一条消息放入消息队列中，主线程不断执行从消息队列取消息，执行的过程。
例如$.ajax()发送异步请求，在工作线程接受到响应后就对应的回调函数封装成一条消息放入消息队列中
```


### Flask.request
简单地理解就是：
1. 你的 current_user_id 应该是根据此次请求的上下文拿到的（比如从 URL 或者 session 中拿），每个请求对应的是不同的 request 上下文
2. 虽然 request 是用 from flask import request 得到的，看起来是共同的一个全局变量，但实际上 flask 用了一个叫 thread local 的方法保证 request 是线程安全的。也就是说，即使在并发场景下，每个人拿到的 request 也是不一样的，处理起来和串行没什么区别。

[参考文献](http://flask.pocoo.org/docs/0.12/quickstart/#accessing-request-data)
还得了解flask的活动上下文


### flask默认变量
>current_app # 当前激活程序的程序实例
>g # 处理请求时用作临时存储的对象。每次请求会重设这个变量
>request # 请求对象，封装了客户端发出的http请求中的内容
>session # 用户会话，用于存储请求之间需要‘记住‘的值的词典

### JQuery 发送json
```javascript
var data = {};
data['id'] = '11';
$.ajax({
    url: 'xxxx',
    dataType: 'json',
    data: data,
    ....
});
```

### 简单异步上传文件
```javascript
<form id="photo-form" class="btn btn-hollow" action="/upload" method='post' enctype='multipart/form-data'>
    <input type="file" id="photo" name="photo" class="hide" onchange="UploadPhoto(this)" accept="image/*">
    更换头像
</form>
$('#photo-form').submit(function(event){
    event.preventDefault(); //禁止默认submit操作
    var form = $(this);
    var formData = new FormData(this);
    $.ajax({
        type: 'post',
        url: '/uploadPhoto',
        mimeType: 'multipart/form-data',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function(photourl){
            alert(photourl);
            $('img').attr('src',photourl);
        },
        error: function(){
            alert('上传失败');
        }
    });
});
```

### 修改submit方式
```javascript
$('#detailModal_form').submit(function(e){
    $(this).ajaxSubmit({
        url: '/dict/update',
        type: 'post',
        data:{
            id: $('#detailModal_id').val(),
            name: $('#detailModal_name').val()
        },
        beforeSubmit: function(formData, jqForm, options){
            //非空检查
            var flag = true;//非空检查结果
            name = formData[1].value;
            if(name.trim() == ""){
                $('#detailModal_name_tip').text('必填');
                flag = false;
            }
            else if (name.length > 50){
                $('#detailModal_name_tip').text('长度不大于50');
                flag = false;
            }
            if(flag)
                $("#detailModal_submit").attr({ disabled: "disabled" });// 禁用按钮防止重复提交
            return flag;
        },
        success: function(data){
            alert("update : " + data);
            if(data == 'success'){
                $("#detailModal").modal("hide");
                $('#table').bootstrapTable('refresh',{url:'/dict/listDictByTypeId?id=' + window.type_id});
            }
        },
        complete: function(){
            $("#detailModal_submit").removeAttr("disabled");
        }
    });
    // always return false to prevent standard browser submit and page navigation 
    return false;//阻止表单默认提交
});
```

### form 与 input
在 form 中的 input 控件，不指定 input 的 name属性，提交表单时时不读取它的数据，指定了 input 的 name 属性后，提交的数据key就是name的值。即name属性用于对提交到服务器后的表单数据进行标识，或者在客户端通过JavaScript引用表单数据。注释：只有设置了name属性的表单元素才能在提交表单时传递他们的值。

> 引申一下 id 和 name 属性的区别
