include $(TOPDIR)/rules.mk
PKG_NAME:=plyvel
PKG_VERSION:=0.9
PKG_RELEASE:=1
PKG_SOURCE:=plyvel-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://pypi.python.org/packages/source/p/plyvel/
PKG_MD5SUM:=b0f768a07683dad01554b040c6320ed5
PKG_BUILD_DIR:=$(BUILD_DIR)/plyvel-$(PKG_VERSION)
PKG_BUILD_DEPENDS:=python
include $(INCLUDE_DIR)/package.mk
$(call include_mk, python-package.mk)
define Package/plyvel
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=plyvel
  URL:=http://pypi.python.org/pypi/plyvel/
  DEPENDS:=+python +python-setuptools +librt +libstdcpp +leveldb
endef

define Package/plyvel/description
  Plyvel, a fast and feature-rich Python interface to LevelDB
endef

define Build/Compile
	$(call Build/Compile/PyMod,, install --prefix="$(PKG_INSTALL_DIR)/usr" )
endef

define Package/plyvel/install
	$(INSTALL_DIR) $(1)$(PYTHON_PKG_DIR)
	$(CP) \
		$(PKG_INSTALL_DIR)$(PYTHON_PKG_DIR)/* \
		$(1)$(PYTHON_PKG_DIR)
endef

$(eval $(call BuildPackage,plyvel))
