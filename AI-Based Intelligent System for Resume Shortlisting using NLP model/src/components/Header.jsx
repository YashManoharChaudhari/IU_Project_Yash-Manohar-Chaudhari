import React from "react";
import { motion } from "framer-motion";
import logoImg from "../assets/hire-assist-logo.png"; // << added

export default function Header() {
  return (
    <header className="site-header">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.55 }}
        className="header-inner"
      >
        <div className="logo"> 
          <img 
            src={logoImg} 
            alt="Hire Assist Logo" 
            className="logo-img" 
            style={{ width: "150px", height: "150px" }} 
          />
  
        </div>
        <p className="subtitle">AI-powered resume shortlisting system</p>
      </motion.div>
    </header>
  );
}