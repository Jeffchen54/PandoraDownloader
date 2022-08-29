# PandoraDownloader

**Status**: Currently is nonfunctional
Redesigned command line downloader. Separate module based downloader where additional services can be added with the use of modules. Design inspired by MVC (Model-View Controller design). 

**Purpose**: A design which allows adding of many different services with minimal edits to existing code. Provide a pathway for GUI development. Design that is easy to expand upon to for upgrading and switching out of components. 

**Early design**:
<img width="1048" alt="image" src="https://user-images.githubusercontent.com/78765964/187277857-b2355bc3-475c-48fd-883d-bd7156149184.png">

Functions have been specifically removed, object contents are highly volatile at this point of development and functions that are displayed should be taken with a grain of salt. 
Basic "UML like" design with arrows showing which component owns what (A->B then B owns A or uses A. Design is subject to change; however, decoupled nature of design will be kept. 

**Services targetted to**: Hard to download services which many popular services either do not support or support poorly (low resolution images, low KB/s download speed)

**Confirmed Services**:
- Kemono Party

**Likely services**:
- Hitomi
- Sankaku
