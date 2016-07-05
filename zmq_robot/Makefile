include $(TOPDIR)/rules.mk

PKG_NAME:=zmq_robot
PKG_VERSION:=0.1
PKG_RELEASE:=1

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)
include $(INCLUDE_DIR)/package.mk
$(call include_mk, python-package.mk)

define Package/zmq_robot
	SUBMENU:=Python
	SECTION:=lang
	CATEGORY:=Languages
	DEFAULT:=n
	TITLE:=Driver creation toolkit for Sensorika robots
	URL:=http://sensorika.info
	DEPENDS:=+python +pyzmq
endef

define Package/zmq_robot/description
	Driver creation toolkit for Sensorika laboratory robots (AMUR-10, Modular robot).
	Uses pyzmq and python's json packages.
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) -R ./files/* $(PKG_BUILD_DIR)/
endef


define Build/Compile
	$(call Build/Compile/PyMod,, install --prefix="$(PKG_INSTALL_DIR)/usr")
endef

define Package/zmq_robot/install
	$(INSTALL_DIR) $(1)$(PYTHON_PKG_DIR)
	$(CP) \
		$(PKG_INSTALL_DIR)$(PYTHON_PKG_DIR)/* \
		$(1)$(PYTHON_PKG_DIR)
endef

$(eval $(call BuildPackage,zmq_robot))
