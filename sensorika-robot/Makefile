include $(TOPDIR)/rules.mk
PKG_NAME:=sensorika-robot
PKG_VERSION:=0.9
PKG_RELEASE:=1
PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/ASMfreaK/sensorika-robot.git
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_VERSION:=239e5a72bfcee4cba812bbb2a385124bb16bc662
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_BUILD_PARALLEL:=1

PKG_BUILD_DIR:=$(BUILD_DIR)/sensorika-robot-$(PKG_VERSION)
PKG_BUILD_DEPENDS:=python
include $(INCLUDE_DIR)/package.mk
$(call include_mk, python-package.mk)
define Package/sensorika-robot
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=sensorika-robot
  URL:=http://github.com/kkirsanov/sensorika-robot
  DEPENDS:=+python +plyvel
endef

define Package/sensorika-robot/description
  Lightweight python middleware library for data exchange between mechatronics components. Sitable for mobile robotics and remote control.
endef

define Build/Compile
	$(call Build/Compile/PyMod,, install --prefix="$(PKG_INSTALL_DIR)/usr")
endef

define Package/sensorika-robot/install
	$(INSTALL_DIR) $(1)$(PYTHON_PKG_DIR)
	$(CP) \
		$(PKG_INSTALL_DIR)$(PYTHON_PKG_DIR)/. \
		$(1)$(PYTHON_PKG_DIR)
endef

$(eval $(call BuildPackage,sensorika-robot))
