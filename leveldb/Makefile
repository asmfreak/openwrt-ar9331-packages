include $(TOPDIR)/rules.mk

PKG_NAME:=leveldb
PKG_VERSION:=v1.18
PKG_RELEASE:=1

#PKG_SOURCE:=iojs-$(PKG_VERSION).tar.gz
#PKG_SOURCE_URL:=https://iojs.org/dist/latest/
#PKG_SHA256SUM:=803d69203a62faf50f1b77897310a3a1fcae712b
PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/google/leveldb.git
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_VERSION:=803d69203a62faf50f1b77897310a3a1fcae712b
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_BUILD_PARALLEL:=1

include $(INCLUDE_DIR)/package.mk

define Package/leveldb
  DEPENDS:=+snappy
  SECTION:=libs
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

define Package/leveldb/install
  $(MAKE) $(PKG_JOBS) -C $(PKG_BUILD_DIR) DESTDIR="$(1)" install
endef

$(eval $(call BuildPackage,leveldb))
