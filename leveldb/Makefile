include $(TOPDIR)/rules.mk

PKG_NAME:=leveldb
PKG_VERSION:=v1.18
PKG_RELEASE:=1

PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/google/leveldb.git
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_VERSION:=803d69203a62faf50f1b77897310a3a1fcae712b
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_BUILD_PARALLEL:=1

include $(INCLUDE_DIR)/package.mk

define Package/leveldb
  DEPENDS:=+snappy +libpthread
  SECTION:=libs
  CATEGORY:=Libraries
  SUBMENU:=database
  TITLE:=A fast and lightweight key/value database library
  URL:=https://github.com/google/leveldb.git
endef

define Package/leveldb/description
	A fast and lightweight key/value database library
endef

define Build/Compile
	$(call Build/Compile/Default)
endef

define Build/InstallDev
	$(INSTALL_DIR) $(STAGING_DIR)/usr/include/leveldb
	$(CP) $(PKG_BUILD_DIR)/include/leveldb/. $(STAGING_DIR)/usr/include/leveldb
	$(INSTALL_DIR) $(1)/usr/lib
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/libleveldb.* $(1)/usr/lib
endef

define Package/leveldb/install
	$(INSTALL_DIR) $(1)/usr/local/lib
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/libleveldb.* $(1)/usr/local/lib
#	$(INSTALL_DIR) $(1)/usr/local/include
#	$(INSTALL_DATA) -d $(PKG_BUILD_DIR)/leveldb $(1)/usr/local/include
endef

$(eval $(call BuildPackage,leveldb))
