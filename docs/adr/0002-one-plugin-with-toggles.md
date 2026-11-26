# One plugin, Components toggled by config

devflow ships as a single plugin; which Components are active is a list in the devflow config, applied by the setup. We considered a marketplace with one plugin per Area, which gives native on/off, but rejected it: the user wants one place to evolve, and Areas are expected to be re-cut often as the workflow changes. Components never call each other directly; they exchange Contracts in the Issue workspace, so turning one off degrades the flow instead of breaking it.
