# Maintainer: Evan Callicoat <apsu@propter.net>
pkgname=python-ordered-set-git
_gitname=ordered-set
pkgver=0.0.0
pkgrel=1
pkgdesc="A python module providing an OrderedSet class."
arch=('i686' 'x86_64')
url="https://github.com/Apsu/ordered-set"
license=('GPL')
depends=('python2')
makedepends=('git' 'python' 'python-setuptools')
provides=('python-ordered-set')
conflicts=('python-ordered-set')
source=('git://github.com/Apsu/ordered-set.git')
md5sums=('SKIP')

pkgver() {
  cd $_gitname
  echo $(git rev-list --count HEAD).$(git rev-parse --short HEAD)
}

build() {
  cd $_gitname

  python setup.py build
}

package() {
  cd $_gitname

  python setup.py install --root="${pkgdir}"
}
