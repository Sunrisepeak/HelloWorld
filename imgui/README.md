# ImGui安卓(Android)示例构建详细步骤

## 0. 环境

- 构建环境: ubuntu 22.04
- 测试环境: Android / XM-13



**注1: Windows系统可以安装WSL(Windows Subsystem for Linux)后在WSL中操作**

**注2: 安装过程中会使用临时环境变量, 请在一个控制台(terminal)下执行命令**



## 1. 基础工具安装

```bash
sudo apt-get install cmake make g++ openjdk-11-jdk git -y
curl -s "https://get.sdkman.io" | bash
sdk install gradle 8.0
# Java - openjdk11
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```



## 2. 安装Android 工具 & SDK & NDK

### 2.1 创建 AndroidHome 目录

> 这个可以替换成自己指定的位置

```bash
mkdir -p ~/android
export ANDROID_HOME=~/android
```



### 2.2 下载&安装安卓commandtools

**设置要下载的版本**

> 其他版本对应的文件名 -> [镜像网站](https://mirrors.cloud.tencent.com/AndroidSDK)

```bash
ANDROID_CMD_TOOLS_FILE=commandlinetools-linux-9123335_latest.zip
```

**下载命令行工具**

```cpp
wget https://mirrors.cloud.tencent.com/AndroidSDK/%ANDROID_CMD_TOOLS_FILE -P $ANDROID_HOME
```

**解压**&配置

```bash
unzip $ANDROID_HOME/$ANDROID_CMD_TOOLS_FILE -d $ANDROID_HOME
ANDROID_SDKMANAGER=$ANDROID_HOME/cmdline-tools/bin/sdkmanager
$ANDROID_SDKMANAGER --version --sdk_root=$ANDROID_HOME
```



### 2.3 使用sdkmanager安装依赖

**同意所有android licenses**

```bash
yes | $ANDROID_SDKMANAGER --licenses --sdk_root=$ANDROID_HOME
```



**安装adb等工具**

```bash
$ANDROID_SDKMANAGER "platform-tools" --sdk_root=$ANDROID_HOME
```



**安装ndk(可选)**

```bash
$ANDROID_SDKMANAGER "ndk;25.2.9519653" --sdk_root=$ANDROID_HOME
```



**安装sdk(可选)**

```bash
$ANDROID_SDKMANAGER "platforms;android-33" --sdk_root=$ANDROID_HOME
```



## 3. 编译ImGui安卓示例

### 3.1 下载示例

**克隆imgui仓库到本地**

```bash
git clone git@github.com:ocornut/imgui.git
```

**cd到Android示例的目录**

```bash
cd imgui/examples/example_android_opengl3/android
```



### 3.2 指定ANDROID_HOME

> 创建local.properties文件, 配置sdk.dir

```bash
echo sdk.dir=$ANDROID_HOME > local.properties
```



### 3.3 编译示例

```bash
gradle assembleDebug --stacktrace
```



## 4. 安装示例APK到手机&运行



### 4.1 验证&安装apk

**连接手机到电脑**

- 需要已经打开调试模式
- 正确通过USB链接到手机

```bash
ANDROID_ADB=$ANDROID_HOME/platform-tools/adb
$ANDROID_ADB devices
```

**安装**

```bash
$ANDROID_ADB install build/outputs/apk/debug/app-debug.apk
```



### 4.2 运行 & 打印log

```bash
$ANDROID_ADB shell am start -n imgui.example.android/.MainActivity
$ANDROID_ADB shell logcat | grep -Ei imgui
```



## 5. 一键自动配置&编译脚本



> [一键编译脚本地址](https://github.com/Sunrisepeak/HelloWorld/blob/main/imgui/android/imgui_android_tools.sh)




### 安装依赖&配置

```bash
./imgui_android_tools.sh install
```

### 编译

```bash
./imgui_android_tools.sh build
```

### 安装&运行apk

```bash
./imgui_android_tools.sh run
```

### 清除编译产物

```bash
./imgui_android_tools.sh clean
```

### 删除所以下载的依赖

> 删除 imgui 代码, 及下载的相关工具和ndk/sdk

```bash
./imgui_android_tools.sh delete
```



## 6. Other

- Repo: https://github.com/Sunrisepeak/HelloWorld
- 一键脚本: https://github.com/Sunrisepeak/HelloWorld/blob/main/imgui/android/imgui_android_tools.sh
- 操作视频: xxx

