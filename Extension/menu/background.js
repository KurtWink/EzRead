/*
Called when the item has been created, or when creation failed due to an error.
We'll just log success/failure here.
*/
function onCreated() {
  if (browser.runtime.lastError) {
    console.log(`Error: ${browser.runtime.lastError}`);
  } else {
    console.log("Item created successfully");
  }
}

/*
Called when the item has been removed.
We'll just log success here.
*/
function onRemoved() {
  console.log("Item removed successfully");
}

/*
Called when there was an error.
We'll just log the error here.
*/
function onError(error) {
  console.log(`Error: ${error}`);
}

/*
Create all the context menu items.
*/

browser.menus.create({
  id: "bluify",
  type: "radio",
  title: browser.i18n.getMessage("menuItemBluify"),
  contexts: ["all"],
  checked: false,
  icons: {
    "16": "icons/paint-blue-16.png",
    "32": "icons/paint-blue-32.png"
  }
}, onCreated);

browser.menus.create({
  id: "separator-2",
  type: "separator",
  contexts: ["all"]
}, onCreated);

var checkedState = true;

browser.menus.create({
  id: "open-EzRead",
  title: browser.i18n.getMessage("menuEzRead"),
  contexts: ["selection"]
}, onCreated);

browser.menus.create({
  id: "open-sidebar",
  title: browser.i18n.getMessage("menuItemOpenSidebar"),
  contexts: ["all"],
  command: "_execute_sidebar_action"
}, onCreated);

browser.menus.create({
  id: "tools-menu",
  title: browser.i18n.getMessage("menuItemToolsMenu"),
  contexts: ["tools_menu"],
}, onCreated);

/*
Set a colored border on the document in the given tab.

Note that this only work on normal web pages, not special pages
like about:debugging.
*/
var blue = 'document.body.style.border = "5px solid blue"';
var green = 'document.body.style.border = "5px solid green"';

function borderify(tabId, color) {
  browser.tabs.executeScript(tabId, {
    code: color
  });
}

/*
Toggle checkedState, and update the menu item's title
appropriately.

Note that we should not have to maintain checkedState independently like
this, but have to because Firefox does not currently pass the "checked"
property into the event listener.
*/
function updateCheckUncheck() {
  checkedState = !checkedState;
  if (checkedState) {
    browser.menus.update("check-uncheck", {
      title: browser.i18n.getMessage("menuItemUncheckMe"),
    });
  } else {
    browser.menus.update("check-uncheck", {
      title: browser.i18n.getMessage("menuItemCheckMe"),
    });
  }
}

/*
The click event listener, where we perform the appropriate action given the
ID of the menu item that was clicked.
*/
browser.menus.onClicked.addListener((info, tab) => {
  switch (info.menuItemId) {
    case "log-selection":
      console.log(info.selectionText);
      break;
    case "bluify":
      borderify(tab.id, blue);
      break;
    case "open-sidebar":
      console.log("Opening my sidebar");
      break;
    case "open-EzRead":
      console.log(info.selectionText);
      break;
    case "tools-menu":
      console.log("Clicked the tools menu item");
      break;
  }
});
