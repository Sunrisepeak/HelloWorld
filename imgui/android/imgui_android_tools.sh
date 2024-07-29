#!/bin/bash
# copyright 2024-present, sunrisepeak
# ubuntu 22.04 tested

# imgui_android_tools.sh install
# imgui_android_tools.sh build
# imgui_android_tools.sh clean
# imgui_android_tools.sh delete

BUILD_DIR=`pwd`/imgui_android_build # Note: don't change

ANDROID_CMD_TOOLS_FILE=commandlinetools-linux-9123335_latest.zip
ANDROID_CMD_TOOLS_DL_LINK="https://mirrors.cloud.tencent.com/AndroidSDK/$ANDROID_CMD_TOOLS_FILE"
ANDROID_HOME_T=$BUILD_DIR/android_home_t
ANDROID_SDKMANAGER=$ANDROID_HOME_T/cmdline-tools/bin/sdkmanager
ANDROID_ADB=$ANDROID_HOME_T/platform-tools/adb

IMGUI_DEMO_DIR=$BUILD_DIR/imgui/examples/example_android_opengl3/android
IMGUI_DEMO_APK=$IMGUI_DEMO_DIR/build/outputs/apk/debug/app-debug.apk

#############################################################

cmd=$1 # install build clean delete

mkdir -p $BUILD_DIR && cd $BUILD_DIR

if [ ! $cmd ]; then
    cmd="build"
fi

if [ $cmd == "install" ] || [ ! -d $ANDROID_HOME_T ]; then
    echo start install && config...

    # basic
    sudo apt-get install cmake make g++ git -y
    sudo apt install openjdk-11-jdk -y

    # check SDKMAN
    if [ -z "$SDKMAN_DIR" ]; then
        echo "SDKMAN not found, installing..."
        curl -s "https://get.sdkman.io" | bash

        # load SDKMAN
        source "$HOME/.sdkman/bin/sdkman-init.sh"
    else
        echo "SDKMAN already installed, initializing..."
        source "$SDKMAN_DIR/bin/sdkman-init.sh"
    fi

    sdk install gradle 7.5

    # imgui
    if [ ! -d "imgui" ]; then
        git clone git@github.com:ocornut/imgui.git
    fi

    # Android

    ## Android Cmd Tools
    if [ ! -d $ANDROID_HOME_T ]; then
        mkdir -p $ANDROID_HOME_T
    fi
    cd $ANDROID_HOME_T

    if [ ! -f $ANDROID_CMD_TOOLS_FILE ]; then
        wget $ANDROID_CMD_TOOLS_DL_LINK
    fi

    if [ ! -d "cmdline-tools" ]; then
        unzip $ANDROID_CMD_TOOLS_FILE
    fi

    export ANDROID_HOME=$ANDROID_HOME_T
    echo Android Home: $ANDROID_HOME

    "$ANDROID_SDKMANAGER" --version --sdk_root=$ANDROID_HOME
    yes | "$ANDROID_SDKMANAGER" --licenses --sdk_root=$ANDROID_HOME

    echo install adb ....
    "$ANDROID_SDKMANAGER" "platform-tools" --sdk_root=$ANDROID_HOME
    #"$ANDROID_SDKMANAGER" "platforms;android-33" --sdk_root=$ANDROID_HOME
    #"$ANDROID_SDKMANAGER" "ndk;25.2.9519653" --sdk_root=$ANDROID_HOME

    echo create local.properties file
    echo sdk.dir=$ANDROID_HOME > $IMGUI_DEMO_DIR/local.properties

    cd $IMGUI_DEMO_DIR
    # install dependencies
    gradle --console=rich

fi

if [ $cmd == "build" ]; then
    echo "imgui android build"
    # imgui demo
    cd $IMGUI_DEMO_DIR
    #gradle build
    gradle assembleDebug --stacktrace --console=rich
    echo Apk Dir: $IMGUI_DEMO_APK
elif [ $cmd == "run" ]; then
    "$ANDROID_ADB" root
    "$ANDROID_ADB" install $IMGUI_DEMO_APK
    "$ANDROID_ADB" shell am start -n imgui.example.android/.MainActivity
    "$ANDROID_ADB" shell logcat | grep -Ei imgui
elif [ $cmd == "clean" ]; then
    cd $IMGUI_DEMO_DIR
    gradle clean
elif [ $cmd == "delete" ]; then
    if [ -d $BUILD_DIR ]; then
        rm -rf $BUILD_DIR
    fi
fi