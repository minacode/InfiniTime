#pragma once
#include <FreeRTOS.h>
#include <queue.h>
#include <task.h>
#include <memory>
#include <systemtask/Messages.h>
#include "displayapp/LittleVgl.h"
#include "displayapp/TouchEvents.h"
#include "components/brightness/BrightnessController.h"
#include "components/motor/MotorController.h"
#include "components/firmwarevalidator/FirmwareValidator.h"
#include "components/settings/Settings.h"
#include "displayapp/screens/Screen.h"
#include "components/timer/Timer.h"
#include "displayapp/ScreenIds.h"
#include "components/alarm/AlarmController.h"
#include "touchhandler/TouchHandler.h"

#include "displayapp/Messages.h"
#include "BootErrors.h"

#include "utility/StaticStack.h"

namespace Pinetime {

  namespace Drivers {
    class St7789;
    class Cst816S;
    class Watchdog;
  }

  namespace Controllers {
    class Settings;
    class Battery;
    class Ble;
    class DateTime;
    class NotificationManager;
    class HeartRateController;
    class MotionController;
    class TouchHandler;
  }

  namespace System {
    class SystemTask;
  };

  namespace Applications {
    class DisplayApp {
    public:
      enum class States { Idle, Running };
      enum class FullRefreshDirections { None, Up, Down, Left, Right, LeftAnim, RightAnim };

      DisplayApp(Drivers::St7789& lcd,
                 const Drivers::Cst816S&,
                 const Controllers::Battery& batteryController,
                 const Controllers::Ble& bleController,
                 Controllers::DateTime& dateTimeController,
                 const Drivers::Watchdog& watchdog,
                 Pinetime::Controllers::NotificationManager& notificationManager,
                 Pinetime::Controllers::HeartRateController& heartRateController,
                 Controllers::Settings& settingsController,
                 Pinetime::Controllers::MotorController& motorController,
                 Pinetime::Controllers::MotionController& motionController,
                 Pinetime::Controllers::AlarmController& alarmController,
                 Pinetime::Controllers::BrightnessController& brightnessController,
                 Pinetime::Controllers::TouchHandler& touchHandler,
                 Pinetime::Controllers::FS& filesystem);
      void Start(System::BootErrors error);
      void PushMessage(Display::Messages msg);

      void StartApp(ScreenId screenId, DisplayApp::FullRefreshDirections direction);

      void SetFullRefresh(FullRefreshDirections direction);

      void Register(Pinetime::System::SystemTask* systemTask);

    private:
      Pinetime::Drivers::St7789& lcd;
      const Pinetime::Drivers::Cst816S& touchPanel;
      const Pinetime::Controllers::Battery& batteryController;
      const Pinetime::Controllers::Ble& bleController;
      Pinetime::Controllers::DateTime& dateTimeController;
      const Pinetime::Drivers::Watchdog& watchdog;
      Pinetime::System::SystemTask* systemTask = nullptr;
      Pinetime::Controllers::NotificationManager& notificationManager;
      Pinetime::Controllers::HeartRateController& heartRateController;
      Pinetime::Controllers::Settings& settingsController;
      Pinetime::Controllers::MotorController& motorController;
      Pinetime::Controllers::MotionController& motionController;
      Pinetime::Controllers::AlarmController& alarmController;
      Pinetime::Controllers::BrightnessController& brightnessController;
      Pinetime::Controllers::TouchHandler& touchHandler;
      Pinetime::Controllers::FS& filesystem;

      Pinetime::Controllers::FirmwareValidator validator;
      Pinetime::Components::LittleVgl lvgl;
      Pinetime::Controllers::Timer timer;

      TaskHandle_t taskHandle;

      States state = States::Running;
      QueueHandle_t msgQueue;

      static constexpr uint8_t queueSize = 10;
      static constexpr uint8_t itemSize = 1;

      std::unique_ptr<Screens::Screen> currentScreen;

      ScreenId currentScreenId = ScreenId::None;
      ScreenId returnToScreenId = ScreenId::None;
      FullRefreshDirections returnDirection = FullRefreshDirections::None;
      TouchEvents returnTouchEvent = TouchEvents::None;

      TouchEvents GetGesture();
      static void Process(void* instance);
      void InitHw();
      void Refresh();
      void LoadNewScreen(ScreenId screenId, DisplayApp::FullRefreshDirections direction);
      void LoadScreen(ScreenId screenId, DisplayApp::FullRefreshDirections direction);
      void PushMessageToSystemTask(Pinetime::System::Messages message);

      ScreenId nextScreenId = ScreenId::None;
      DisplayApp::FullRefreshDirections nextDirection;
      System::BootErrors bootError;
      void ApplyBrightness();

      static constexpr size_t returnStackSize = 10;
      Utility::StaticStack<ScreenId, returnStackSize> returnStack;
      Utility::StaticStack<FullRefreshDirections, returnStackSize> stackDirections;

      bool isDimmed = false;
    };
  }
}
