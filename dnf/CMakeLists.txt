FILE(GLOB dnf_SRCS *.py)
INSTALL (FILES ${dnf_SRCS} DESTINATION ${PYTHON_INSTALL_DIR}/dnf)
ADD_SUBDIRECTORY (rpmUtils)
ADD_SUBDIRECTORY (yum)
ADD_SUBDIRECTORY (cli)
